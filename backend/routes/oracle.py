from flask import Blueprint, request, jsonify
from web3 import Web3
import time

from services.database import get_db_connection
from services.blockchain import w3
from routes.auth import token_required

oracle_bp = Blueprint("oracle", __name__)


@oracle_bp.route("/oracle/device/register", methods=["POST"])
def register_device():
    data = request.get_json()
    device_id = data.get("device_id")
    public_key = data.get("public_key")
    owner_address = data.get("owner_address")
    location_lat = data.get("location_lat")
    location_lon = data.get("location_lon")

    if not device_id or not public_key or not owner_address:
        return jsonify(
            {"error": "device_id, public_key, and owner_address required"}
        ), 400

    if not Web3.is_address(owner_address):
        return jsonify({"error": "Invalid owner address"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO devices (device_id, public_key, owner_address, location_lat, location_lon)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (device_id) DO UPDATE SET
                   public_key = EXCLUDED.public_key,
                   owner_address = EXCLUDED.owner_address,
                   location_lat = EXCLUDED.location_lat,
                   location_lon = EXCLUDED.location_lon,
                   status = 'active'
                   RETURNING device_id""",
                (device_id, public_key, owner_address, location_lat, location_lon),
            )
            conn.commit()
            return jsonify({"status": "success", "device_id": device_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


@oracle_bp.route("/oracle/device/<device_id>", methods=["GET"])
def get_device(device_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT device_id, public_key, owner_address, location_lat, location_lon, status, last_seen, registered_at
                   FROM devices WHERE device_id = %s""",
                (device_id,),
            )
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "Device not found"}), 404

            return jsonify(
                {
                    "device_id": row[0],
                    "public_key": row[1],
                    "owner_address": row[2],
                    "location_lat": float(row[3]) if row[3] else None,
                    "location_lon": float(row[4]) if row[4] else None,
                    "status": row[5],
                    "last_seen": row[6].isoformat() if row[6] else None,
                    "registered_at": row[7].isoformat() if row[7] else None,
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


@oracle_bp.route("/oracle/device/owner/<owner_address>", methods=["GET"])
def get_devices_by_owner(owner_address):
    if not Web3.is_address(owner_address):
        return jsonify({"error": "Invalid address"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT device_id, status, registered_at, last_seen
                   FROM devices WHERE owner_address = %s""",
                (owner_address,),
            )
            rows = cur.fetchall()
            devices = []
            for row in rows:
                devices.append(
                    {
                        "device_id": row[0],
                        "status": row[1],
                        "registered_at": row[2].isoformat() if row[2] else None,
                        "last_seen": row[3].isoformat() if row[3] else None,
                    }
                )
            return jsonify({"devices": devices})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


@oracle_bp.route("/oracle/energy/submit", methods=["POST"])
def submit_energy():
    data = request.get_json()
    device_id = data.get("device_id")
    timestamp = data.get("timestamp")
    energy_kwh = data.get("energy_kwh")
    signature = data.get("signature")

    if not all([device_id, timestamp, energy_kwh, signature]):
        return jsonify(
            {"error": "device_id, timestamp, energy_kwh, signature required"}
        ), 400

    submission_hash = w3.keccak(text=f"{device_id}:{timestamp}:{energy_kwh}").hex()

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT device_id, public_key, status FROM devices WHERE device_id = %s",
                (device_id,),
            )
            device = cur.fetchone()
            if not device:
                return jsonify({"error": "Device not registered"}), 404
            if device[2] != "active":
                return jsonify({"error": f"Device is {device[2]}"}), 400

            cur.execute(
                "SELECT id FROM energy_submissions WHERE submission_hash = %s",
                (submission_hash,),
            )
            if cur.fetchone():
                return jsonify({"error": "Duplicate submission"}), 400

            current_time = int(time.time())
            if abs(timestamp - current_time) > 86400:
                return jsonify({"error": "Timestamp too old or in future"}), 400

            cur.execute(
                """INSERT INTO energy_submissions (device_id, timestamp, energy_kwh, signature, submission_hash)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (device_id, timestamp, energy_kwh, signature, submission_hash),
            )
            conn.commit()

            return jsonify(
                {
                    "status": "submitted",
                    "submission_hash": submission_hash,
                    "message": "Submission received, awaiting verification",
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


@oracle_bp.route("/oracle/energy/pending", methods=["GET"])
@token_required
def get_pending_submissions():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, device_id, timestamp, energy_kwh, signature
                   FROM energy_submissions
                   WHERE verified = FALSE
                   AND created_at > NOW() - INTERVAL '1 hour'
                   ORDER BY timestamp ASC
                   LIMIT 100"""
            )
            rows = cur.fetchall()
            submissions = []
            for row in rows:
                submissions.append(
                    {
                        "id": row[0],
                        "device_id": row[1],
                        "timestamp": row[2],
                        "energy_kwh": float(row[3]),
                        "signature": row[4],
                    }
                )

            return jsonify({"count": len(submissions), "submissions": submissions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
