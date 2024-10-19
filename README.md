# MECC Umbane Token System

This project implements a token system for the MECC Umbane Energy initiative, utilizing the Polygon Matic blockchain. Umbane means electricity in isiXhosa.

## Current Status

*   **Smart Contracts:**  The Solidity smart contract (`contracts/Token.sol`) is implemented with functions for minting, burning, and checking balances for both mJ (energy) and aC (carbon credit) tokens.
*   **Backend API:** A Flask-based backend API (`backend/app.py`) is partially implemented.  It includes a `mintMJ` endpoint with basic database integration for transaction logging.  Additional endpoints and more robust error handling are needed.
*   **Frontend:** A basic React frontend (`frontend/App.js`) is in place.  Further development is required to create a user interface for interacting with the backend API.
*   **Database:** A PostgreSQL database needs to be set up.
*   **Chainlink Integration:**  Chainlink integration for oracle functionality is pending.
* **Carbon Credit Trading Gateway** A gateway to the Johnnesburg Stock Exchange (JSE) Carbon Credit Trading desk API is proposed.

## Next Steps

1.  Complete the backend API (add remaining endpoints, improve error handling, and add authentication).
2.  Implement the frontend (create a user interface for interacting with the backend API).
3.  Integrate Chainlink (research and implement a suitable method for interacting with Chainlink oracles).
4.  Set up the PostgreSQL database.
5.  Deploy the smart contract to the Polygon network.
6. Integrate the JSE carbon trading API
7.  Test thoroughly.
