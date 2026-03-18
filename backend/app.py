from flask import Flask, request, jsonify
import psycopg2
import os
from web3 import Web3
from functools import wraps
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

DATABASE_URL = (
    os.environ.get("DATABASE_URL") or "postgresql://user:password@localhost:5432/umbane"
)
SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

w3 = Web3(
    Web3.HTTPProvider(
        os.environ.get("POLYGON_PROVIDER_URL", "https://rpc-amoy.polygon.tech")
    )
)
contract_address = os.environ.get(
    "CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000"
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
        "inputs": [{"name": "amount", "type": "uint256"}],
        "name": "burnMJ",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "amount", "type": "uint256"}],
        "name": "burnAC",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "getMJBalance",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "getACBalance",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)
account_address = os.environ.get(
    "ACCOUNT_ADDRESS", "0x0000000000000000000000000000000000000000"
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


@app.route("/balance/<token_type>/<address>", methods=["GET"])
@token_required
def get_balance(token_type, address):
    if not Web3.is_address(address):
        return jsonify({"error": "Invalid address"}), 400

    if token_type not in ["mJ", "aC"]:
        return jsonify({"error": "Invalid token type"}), 400

    try:
        if token_type == "mJ":
            balance = contract.functions.getMJBalance(address).call()
        else:
            balance = contract.functions.getACBalance(address).call()

        return jsonify(
            {"address": address, "token_type": token_type, "balance": balance}
        )
    except Exception as e:
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
