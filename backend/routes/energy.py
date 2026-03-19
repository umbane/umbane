from flask import Blueprint, request, jsonify
from web3 import Web3

from services.blockchain import contract, w3, account_address
from routes.auth import token_required

energy_bp = Blueprint("energy", __name__)


@energy_bp.route("/chainlink/price-feed/set", methods=["POST"])
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
                "block_number": tx_receipt["blockNumber"],
                "status": "success",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@energy_bp.route("/chainlink/price-feed/update", methods=["POST"])
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


@energy_bp.route("/chainlink/price-feed/get", methods=["GET"])
@token_required
def get_carbon_price():
    try:
        price_data = contract.functions.getCarbonPrice().call()
        return jsonify({"price": price_data[0], "timestamp": price_data[1]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@energy_bp.route("/chainlink/calculate-credits", methods=["GET"])
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


@energy_bp.route("/chainlink/carbon-value", methods=["GET"])
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


@energy_bp.route("/chainlink/process-energy", methods=["POST"])
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
