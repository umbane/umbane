# Umbane Token System Setup Guide

## Prerequisites

1. **Node.js** (for frontend)
2. **Python 3.11+** (for backend)
3. **Foundry** (for smart contract deployment)
4. **PostgreSQL** (optional - for local development)

---

## Wallet & Keys

### Private Key

Your Ethereum wallet private key is required to sign deployment transactions.

**To get from MetaMask:**
1. Open MetaMask extension
2. Click account icon (top-right) → "Account details"
3. Click "Show private key"
4. Enter password
5. Copy the 64-character hex string (starts with `0x`)

**⚠️ SECURITY:**
- Never commit this to git
- Keep it safe - anyone with this key controls the contract
- Use a separate wallet for testing, not your main wallet

---

## Blockchain Networks

### Polygon Amoy Testnet

**RPC URL:** `https://rpc-amoy.polygon.tech`

**Chain ID:** 80002

**Explorer:** https://amoy.polygonscan.com/

**Get Testnet MATIC:**
1. Go to https://faucet.polygon.technology/
2. Connect wallet (make sure you're on Amoy)
3. Request testnet MATIC

---

## Environment Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/umbane/umbane.git
cd umbane

# Backend
cd backend
uv venv
uv pip install -r requirements.txt

# Frontend
cd ../frontend
npm install

# Smart Contracts
cd ..
forge install
```

### 2. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit with your values
nano .env
```

**Required in `.env`:**
```bash
# Your wallet private key (0x...)
PRIVATE_KEY=0x...

# Polygon Amoy RPC URL
POLYGON_AMOX_RPC_URL=https://rpc-amoy.polygon.tech
```

### 3. Deploy Contract

```bash
# Build contracts
forge build

# Deploy to Amoy testnet
forge script script/Deploy.s.sol --rpc-url polygon_amoy --broadcast
```

**Save the contract address** from the output - you'll need it for the backend.

### 4. Configure Backend

Set these environment variables:
```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/umbane
export POLYGON_PROVIDER_URL=https://rpc-amoy.polygon.tech
export CONTRACT_ADDRESS=<deployed_contract_address>
export ACCOUNT_ADDRESS=<your_wallet_address>
export ACCOUNT_PRIVATE_KEY=<your_private_key>
```

### 5. Set Up Database

```bash
# Create database
createdb umbane

# Run schema
psql $DATABASE_URL -f database/schema.sql
```

### 6. Run Backend

```bash
cd backend
source .venv/bin/activate
python app.py
```

### 7. Run Frontend

```bash
cd frontend
npm start
```

---

## Contract Upgradeability

The deployed contract uses **UUPS upgradeable proxy pattern**:

| Capability | Supported |
|-----------|-----------|
| Upgrade contract logic | ✅ Yes |
| Add new functions | ✅ Yes |
| Change storage layout | ⚠️ Careful |
| Recover stuck funds | ✅ Yes |
| Transfer ownership | ✅ Yes |

**To upgrade:**
1. Modify `contracts/Token.sol`
2. Deploy new implementation:
   ```bash
   forge script script/Deploy.s.sol --rpc-url polygon_amoy --broadcast
   ```
3. Call `upgradeTo()` on proxy (requires owner)

---

## Post-Deployment Checklist

- [ ] Contract verified on Polygonscan
- [ ] Backend `CONTRACT_ADDRESS` updated
- [ ] Test mint/burn from backend
- [ ] Frontend connects and displays balances
- [ ] Chainlink VRF configured (subscription)
- [ ] Carbon price feed configured

---

## Troubleshooting

**"Insufficient funds"**
- Get more MATIC from faucet

**"Connection refused"**
- Check RPC URL is correct

**"Nonce too low"**
- Reset your account in MetaMask or use `--priority-fee`

**Contract verification**
```bash
forge verify-contract <address> --chain polygon_amoy
```
