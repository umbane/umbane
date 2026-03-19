from flask import Blueprint, request, jsonify
from web3 import Web3
import jwt
from datetime import datetime, timedelta
from functools import wraps

from services.database import get_db_connection

SECRET_KEY = "dev-secret-key-change-in-production"

auth_bp = Blueprint("auth", __name__)


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


@auth_bp.route("/auth/login", methods=["POST"])
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
