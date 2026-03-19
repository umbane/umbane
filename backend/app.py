from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from web3 import Web3
from functools import wraps
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DATABASE_URL = (
    os.environ.get("DATABASE_URL")
    or "postgresql://umbane:password@localhost:5432/carbon"
)
SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

w3 = Web3(
    Web3.HTTPProvider(
        os.environ.get("POLYGON_PROVIDER_URL")
        or os.environ.get("POLYGON_AMOY_RPC_URL")
        or "https://rpc.ankr.com/polygon_amoy/d06f5dee9abc00217a93067745b34f68bae7d0349a74556a00450163c96615a4"
    )
)
contract_address = os.environ.get(
    "CONTRACT_ADDRESS", "0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe"
)

contract_abi = [
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "mintMJ",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "mintAC",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "amount", "type": "uint256"},
        ],
        "name": "burnMJ",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "amount", "type": "uint256"},
        ],
        "name": "burnAC",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "user", "type": "address"},
            {"name": "energyUsed", "type": "uint256"},
        ],
        "name": "recordEnergyUsage",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "user", "type": "address"},
        ],
        "name": "processEnergyRecord",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "_feedAddress", "type": "address"}],
        "name": "setCarbonPriceFeed",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [],
        "name": "updateCarbonPrice",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getCarbonPrice",
        "outputs": [
            {"name": "", "type": "int256"},
            {"name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "energyKWh", "type": "uint256"}],
        "name": "calculateCarbonCredits",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [{"name": "acAmount", "type": "uint256"}],
        "name": "getCarbonValueUSD",
        "outputs": [{"name": "", "type": "int256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)
account_address = os.environ.get(
    "ACCOUNT_ADDRESS", "0x5Ee264d83332Ba0Cf46f8b1EB7B064e34d62d7Dc"
)
account_private_key = os.environ.get("ACCOUNT_PRIVATE_KEY", "")


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    return conn


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            if token.startswith("Bearer "):
                token = token[7:]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated


@app.route("/health", methods=["GET"])
def health_check():
    db_status = "connected" if get_db_connection() else "disconnected"
    web3_status = "connected" if w3.is_connected() else "disconnected"
    return jsonify({"status": "ok", "database": db_status, "web3": web3_status})


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    wallet_address = data.get("wallet_address")
    signature = data.get("signature")

    if not wallet_address or not signature:
        return jsonify({"error": "wallet_address and signature required"}), 400

    if not Web3.is_address(wallet_address):
        return jsonify({"error": "Invalid wallet address"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM users WHERE wallet_address = %s", (wallet_address,)
            )
            user = cur.fetchone()
            if not user:
                cur.execute(
                    "INSERT INTO users (wallet_address) VALUES (%s) RETURNING id",
                    (wallet_address,),
                )
                conn.commit()

            token = jwt.encode(
                {
                    "wallet_address": wallet_address,
                    "exp": datetime.utcnow() + timedelta(hours=24),
                },
                SECRET_KEY,
                algorithm="HS256",
            )

            return jsonify({"token": token, "wallet_address": wallet_address})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


def log_transaction(address, token_type, amount, tx_type, tx_hash=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO transactions (user_address, token_type, amount, type, tx_hash)
                   VALUES (%s, %s, %s, %s, %s)""",
                (address, token_type, amount, tx_type, tx_hash),
            )
            conn.commit()
    finally:
        if conn:
            conn.close()


@app.route("/mintMJ", methods=["POST"])
@token_required
def mint_mj():
    data = request.get_json()
    address = data.get("address")
    amount = data.get("amount")

    if not address or not amount:
        return jsonify({"error": "address and amount required"}), 400

    if not Web3.is_address(address):
        return jsonify({"error": "Invalid address"}), 400

    try:
        amount = int(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        tx_hash = contract.functions.mintMJ(address, amount).transact(
            {"from": account_address}
        )
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        log_transaction(address, "mJ", amount, "mint", tx_hash.hex())

        return jsonify(
            {
                "tx_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/mintAC", methods=["POST"])
@token_required
def mint_ac():
    data = request.get_json()
    address = data.get("address")
    amount = data.get("amount")

    if not address or not amount:
        return jsonify({"error": "address and amount required"}), 400

    if not Web3.is_address(address):
        return jsonify({"error": "Invalid address"}), 400

    try:
        amount = int(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        tx_hash = contract.functions.mintAC(address, amount).transact(
            {"from": account_address}
        )
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        log_transaction(address, "aC", amount, "mint", tx_hash.hex())

        return jsonify(
            {
                "tx_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/burnMJ", methods=["POST"])
@token_required
def burn_mj():
    data = request.get_json()
    amount = data.get("amount")

    if not amount:
        return jsonify({"error": "amount required"}), 400

    try:
        amount = int(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        tx_hash = contract.functions.burnMJ(amount).transact({"from": account_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        log_transaction(account_address, "mJ", amount, "burn", tx_hash.hex())

        return jsonify(
            {
                "tx_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/burnAC", methods=["POST"])
@token_required
def burn_ac():
    data = request.get_json()
    amount = data.get("amount")

    if not amount:
        return jsonify({"error": "amount required"}), 400

    try:
        amount = int(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        tx_hash = contract.functions.burnAC(amount).transact({"from": account_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        log_transaction(account_address, "aC", amount, "burn", tx_hash.hex())

        return jsonify(
            {
                "tx_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/total-supply", methods=["GET"])
@token_required
def get_total_supply():
    try:
        supply = contract.functions.totalSupply().call()
        return jsonify({"totalSupply": supply})
    except Exception as e:
        print(f"Total supply error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/balance/<token_type>/<address>", methods=["GET"])
@token_required
def get_balance(token_type, address):
    if not Web3.is_address(address):
        return jsonify({"error": "Invalid address"}), 400

    if token_type not in ["mJ", "aC"]:
        return jsonify({"error": "Invalid token type"}), 400

    try:
        balance = contract.functions.balanceOf(address).call()
        return jsonify(
            {"address": address, "token_type": token_type, "balance": balance}
        )
    except Exception as e:
        print(f"Balance error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/transactions/<address>", methods=["GET"])
@token_required
def get_transactions(address):
    if not Web3.is_address(address):
        return jsonify({"error": "Invalid address"}), 400

    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, token_type, amount, type, tx_hash, created_at
                   FROM transactions WHERE user_address = %s
                   ORDER BY created_at DESC LIMIT %s OFFSET %s""",
                (address, limit, offset),
            )
            rows = cur.fetchall()

            transactions = []
            for row in rows:
                transactions.append(
                    {
                        "id": row[0],
                        "token_type": row[1],
                        "amount": str(row[2]),
                        "type": row[3],
                        "tx_hash": row[4],
                        "created_at": row[5].isoformat() if row[5] else None,
                    }
                )

            return jsonify({"transactions": transactions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


@app.route("/chainlink/price-feed/set", methods=["POST"])
@token_required
def set_carbon_price_feed():
    data = request.get_json()
    feed_address = data.get("feed_address")

    if not feed_address:
        return jsonify({"error": "feed_address required"}), 400

    if not Web3.is_address(feed_address):
        return jsonify({"error": "Invalid feed address"}), 400

    try:
        tx_hash = contract.functions.setCarbonPriceFeed(feed_address).transact(
            {"from": account_address}
        )
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify(
            {
                "tx_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chainlink/price-feed/update", methods=["POST"])
@token_required
def update_carbon_price():
    try:
        tx_hash = contract.functions.updateCarbonPrice().transact(
            {"from": account_address}
        )
        w3.eth.wait_for_transaction_receipt(tx_hash)
        price_data = contract.functions.getCarbonPrice().call()
        return jsonify(
            {
                "tx_hash": tx_hash.hex(),
                "price": price_data[0],
                "timestamp": price_data[1],
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chainlink/price-feed/get", methods=["GET"])
@token_required
def get_carbon_price():
    try:
        price_data = contract.functions.getCarbonPrice().call()
        return jsonify({"price": price_data[0], "timestamp": price_data[1]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chainlink/calculate-credits", methods=["GET"])
def calculate_carbon_credits():
    energy_kwh = request.args.get("energy_kwh", type=int)
    if not energy_kwh:
        return jsonify({"error": "energy_kwh parameter required"}), 400

    try:
        credits = energy_kwh * 500
        return jsonify(
            {
                "energy_kwh": energy_kwh,
                "credits": str(credits),
                "calculation": f"{energy_kwh} kWh × 500g CO2/kWh = {credits}g CO2 offset",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chainlink/carbon-value", methods=["GET"])
@token_required
def get_carbon_value():
    ac_amount = request.args.get("amount", type=int)
    if not ac_amount:
        return jsonify({"error": "amount parameter required"}), 400

    try:
        value = contract.functions.getCarbonValueUSD(ac_amount).call()
        return jsonify(
            {
                "ac_amount": ac_amount,
                "usd_value": value,
                "note": "Value in USD (assuming price feed is set)",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chainlink/process-energy", methods=["POST"])
@token_required
def process_energy_record():
    data = request.get_json()
    user_address = data.get("user_address")

    if not user_address:
        return jsonify({"error": "user_address required"}), 400

    if not Web3.is_address(user_address):
        return jsonify({"error": "Invalid user address"}), 400

    try:
        pending = contract.functions.getUserPendingCredits(user_address).call()
        if pending == 0:
            return jsonify({"pending_credits": 0, "message": "No pending credits"})

        tx_hash = contract.functions.processEnergyRecord(user_address).transact(
            {"from": account_address}
        )
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify(
            {"tx_hash": tx_hash.hex(), "minted_credits": pending, "status": "success"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============ ESP Oracle Device Registration ============


@app.route("/oracle/device/register", methods=["POST"])
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


@app.route("/oracle/device/<device_id>", methods=["GET"])
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


@app.route("/oracle/device/owner/<owner_address>", methods=["GET"])
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


@app.route("/oracle/energy/submit", methods=["POST"])
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

            import time

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


@app.route("/oracle/energy/pending", methods=["GET"])
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
