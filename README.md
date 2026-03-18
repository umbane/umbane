# Umbane - Carbon Credit Token System

[Umbane](https://glosbe.com/xh/en/umbane) means electricity in isiXhosa.

A carbon credit token system built on Polygon Amoy that enables prosumer energy producers to earn carbon credits for renewable energy generation.

## Overview

This project enables household solar/wind energy producers to:
1. Submit energy production data (via meters or ESP32 devices)
2. Receive UMB tokens (mJ) based on verified watts produced
3. Exchange UMB for carbon credits (aC) via trading desks
4. Pledge tokens to earn CarB community rewards

## Architecture

```
┌─────────────────┐     ┌─────────────┐     ┌──────────────────┐
│  ESP32/Meter    │────▶│  Chainlink  │────▶│  Smart Contract  │
│  Data Acquistion│     │   Oracle    │     │  (Polygon Amoy)  │
└─────────────────┘     └─────────────┘     └──────────────────┘
                                                        │
                        ┌─────────────┐                 │
                        │   Backend   │◀────────────────┘
                        │  (Flask)    │
                        └─────────────┘
                               │
                        ┌─────────────┐
                        │   Frontend  │
                        │   (React)   │
                        └─────────────┘
```

## Current Status

| Component | Status | Location |
|-----------|--------|----------|
| Smart Contract | ✅ Deployed | `contracts/Token.sol` |
| Backend API | ✅ Complete | `backend/app.py` |
| Frontend UI | ✅ Complete | `frontend/src/App.js` |
| PostgreSQL | ✅ Local | `carbon` database |
| Token (UMB) | ✅ On Polygon Amoy | `0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe` |
| Chainlink | 🔄 Research | See issues |
| Production Deploy | 🔄 Pending | - |

## Token System

- **mJ / UMB**: Energy token - minted per watt of production (1W = 1 UMB)
- **aC**: Carbon credit - obtained by exchanging UMB at trading desk
- **CarB**: Pledge reward - created from UMB + aC, earns community rewards

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.12+
- PostgreSQL
- MetaMask wallet

### Backend Setup

```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Create database
psql -U umbane -h localhost -d carbon -c "CREATE TABLE users (...);"

# Run server
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Environment Variables

Create `.env` in backend directory:

```
DATABASE_URL=postgresql://umbane:password@localhost:5432/carbon
POLYGON_AMOY_RPC_URL=https://rpc.ankr.com/polygon_amoy/...
PRIVATE_KEY=your_private_key
ACCOUNT_ADDRESS=your_wallet_address
CONTRACT_ADDRESS=0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/auth/login` | POST | Wallet authentication |
| `/balance/{type}/{address}` | GET | Get token balance |
| `/total-supply` | GET | Get total supply |
| `/mintMJ` | POST | Mint tokens (owner) |
| `/burnMJ` | POST | Burn tokens (owner) |
| `/chainlink/calculate-credits` | GET | Calculate credits from energy |

## Smart Contract

**UMB Token**: `0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe`
- Network: Polygon Amoy Testnet
- Explorer: https://amoy.polygonscan.com/token/0xF5D3E95244e07444eCFfE9BF04418cF1Fe398aDe

## Related Projects

- [carbon-project](https://github.com/umbane/carbon-project) - ESP32 firmware, smart meter data acquisition, full system design
- [mecc.org.za](https://github.com/umbane/mecc.org.za) - MECC website (Netlify)

## Roadmap

See [issues](https://github.com/umbane/umbane/issues) for current tasks:

1. **P1**: Deploy to production (Render + Vercel/Netlify)
2. **P1**: Implement Chainlink oracle for energy verification
3. **P1**: Research local carbon trading (JSE, City Power)
4. **P2**: Carbonmark API integration
5. **P2**: ESP32 hardware design

## Documentation

- [API Documentation](docs/API.md)
- [Setup Guide](docs/SETUP.md)
- [Carbon Market Research](docs/carbon-market-research.md)
- [Ghost Tokens Research](docs/ghost-tokens-research.md)

## License

GNU General Public License v3.0
