from flask import Blueprint, request, jsonify
from web3 import Web3

from services.database import get_db_connection
from services.blockchain import contract, w3, account_address
from routes.auth import token_required

tokens_bp = Blueprint("tokens", __name__)


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


@tokens_bp.route("/mintMJ", methods=["POST"])
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
                "block_number": tx_receipt["blockNumber"],
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tokens_bp.route("/mintAC", methods=["POST"])
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
                "block_number": tx_receipt["blockNumber"],
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tokens_bp.route("/burnMJ", methods=["POST"])
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
                "block_number": tx_receipt["blockNumber"],
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tokens_bp.route("/burnAC", methods=["POST"])
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
                "block_number": tx_receipt["blockNumber"],
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tokens_bp.route("/total-supply", methods=["GET"])
@token_required
def get_total_supply():
    try:
        supply = contract.functions.totalSupply().call()
        return jsonify({"totalSupply": supply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tokens_bp.route("/balance/<token_type>/<address>", methods=["GET"])
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
        return jsonify({"error": str(e)}), 500


@tokens_bp.route("/transactions/<address>", methods=["GET"])
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
