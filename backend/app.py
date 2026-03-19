from flask import Flask, jsonify
from flask_cors import CORS

from services.database import get_db_connection
from routes.auth import auth_bp
from routes.tokens import tokens_bp
from routes.oracle import oracle_bp
from routes.energy import energy_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(tokens_bp)
app.register_blueprint(oracle_bp)
app.register_blueprint(energy_bp)


@app.route("/health", methods=["GET"])
def health_check():
    db_status = "connected" if get_db_connection() else "disconnected"
    return jsonify({"status": "ok", "database": db_status})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
