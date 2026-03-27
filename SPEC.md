# Umbane Technical Specification

**Version:** 1.0  
**Date:** March 27, 2026  
**Status:** Draft

---

## 1. Project Overview

Umbane is a tokenized on-chain carbon and energy system for South African prosumers. It enables households with solar installations to monetize clean energy production as verifiable carbon credits (aC) and tradeable energy tokens (mJ).

**Mission:** Disintermediate expensive REC registries (zaREC: R25,000/device, I-REC: £800-2,500/device) by creating a parallel tokenized system with optional bridges to traditional carbon markets.

---

## 2. Technology Stack

### 2.1 Blockchain
| Layer | Technology | Network |
|-------|------------|---------|
| Smart Contracts | Solidity | Polygon Amoy (80002) → Mainnet (137) |
| Token Standards | ERC-20 (mJ), ERC-721 (aC) | OpenZeppelin | Note: Token design pending - see Section 4.1 |
| Oracle | Chainlink | Price feeds + VRF |
| DEX | Uniswap V3 | QuickSwap/SushiSwap |

### 2.2 Backend
| Component | Technology |
|-----------|------------|
| API Framework | Python FastAPI |
| Database | PostgreSQL |
| Authentication | JWT (auth/login endpoint) |
| Message Queue | Redis (for batch processing) |

### 2.3 Frontend
| Component | Technology |
|-----------|------------|
| Framework | React 18 |
| Web3 | ethers.js / wagmi |
| Styling | CSS Modules |
| Build | Vite |

### 2.4 Hardware
| Component | Model | Purpose |
|-----------|-------|---------|
| CT Clamp | SCT-013-030 (30A) / SCT-013-100 (100A) | Current measurement |
| Power Module | PZEM-004T | V, A, W, Hz, PF measurement |
| Microcontroller | ESP32-WROOM-32 | Data collection, signing, transmission |
| Communication | LoRa (Ra-01 SX1278) / WiFi | Data transmission |

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PHYSICAL LAYER                                  │
│  Solar Panel → CT Clamp → PZEM-004T → ESP32 → LoRa/WiFi                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           COMMUNICATION LAYER                               │
│  LoRa Gateway → Backend API → Chainlink Oracle                               │
│  (2-15km range)    (FastAPI)     (Verification)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          BLOCKCHAIN LAYER (Polygon)                         │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Token.sol   │  │ Governor.sol │  │  Oracle.sol  │  │  Bridge.sol  │    │
│  │ mJ + aC ERC20 │  │    DAO       │  │ Price Feeds  │  │  COAS/JSE    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DEFI LAYER                                     │
│  ┌────────────────────────┐  ┌────────────────────────────────────────┐     │
│  │  Uniswap V3 Pools      │  │  Liquidity Mining (UMBANE rewards)   │     │
│  │  aC/USDC, mJ/MATIC     │  │  LP staking, aC staking              │     │
│  └────────────────────────┘  └────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             USER LAYER                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Dashboard  │  │  Trading    │  │    DAO      │  │    Grid     │        │
│  │   (React)   │  │   Desk      │  │ Governance  │  │  Purchase   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Smart Contract Specifications

### 4.1 Token.sol

**Location:** `contracts/Token.sol`

**Design Decision (IMPLEMENTED):** Both tokens are currently ERC-20 (Option C below). This differs from original spec which showed aC as ERC-721 NFT.

| Option | mJ Token | aC Token | Status |
|--------|----------|----------|--------|
| **A: Current (aC NFT)** | ERC-20 | ERC-721 NFT | Not implemented |
| **B: Dual Process** | ERC-721 NFT | ERC-20 | Not implemented |
| **C: Simple (both ERC-20)** | ERC-20 | ERC-20 | ✓ **IMPLEMENTED** |

**Current Implementation (Token.sol):**
- Uses OpenZeppelin ERC20Upgradeable (upgradeable)
- Both mJ and aC use same token (via `mintMJ` and `mintAC` functions)
- Single token contract, two internal accounting tracks
- Emission factor: 500g CO2/kWh (older spec says 0.9kg, needs update)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Token is ERC20, ERC721, Ownable {
    
    // State Variables
    uint256 public mJTotalSupply;
    uint256 public aCTotalSupply;
    int256 public latestCarbonPrice;      // USD/kg
    uint256 public electricityTariff;      // ZAR/kWh
    
    // Mappings
    mapping(address => uint256) public mJBalanceOf;
    mapping(address => uint256[]) public userACTokens;
    mapping(address => EnergyRecord[]) public userEnergyHistory;
    mapping(address => uint256) public pendingCarbonCredits;
    mapping(bytes32 => bool) public processedSignatures;
    
    // Structs
    struct EnergyRecord {
        uint256 kWh;
        uint256 timestamp;
        bytes32 signatureHash;
    }
    
    struct CarbonCredit {
        uint256 kgCO2;
        uint256 vintage;
        string methodology;
        bytes32 deviceId;
        bool retired;
    }
    mapping(uint256 => CarbonCredit) public carbonCredits;
    
    // Events
    event MJMinted(address indexed to, uint256 amount);
    event ACMinted(address indexed to, uint256 tokenId, uint256 kgCO2);
    event EnergyRecorded(address indexed user, uint256 kWh, uint256 timestamp);
    event TokenRetired(address indexed user, uint256 tokenId, uint256 kgCO2, string certificateId);
    event CarbonPriceUpdated(int256 price);
    event ElectricityTariffUpdated(uint256 newTariff);
    event BridgeToCOAS(address indexed user, uint256[] tokenIds, bytes32 merkleRoot);
    
    // Constructor
    constructor() ERC20("Umbane Energy", "mJ") ERC721("Umbane Carbon", "aC") Ownable(msg.sender) {}
    
    // Functions
    function recordEnergyUsage(address user, uint256 kWh, bytes32 signatureHash) external onlyOwner {
        uint256 mJAmount = kWh * 1000000; // 1 kWh = 1,000,000 mJ
        mJBalanceOf[user] += mJAmount;
        mJTotalSupply += mJAmount;
        
        uint256 pendingKG = (kWh * 90) / 100; // 0.9 kg CO2/kWh
        pendingCarbonCredits[user] += pendingKG;
        
        userEnergyHistory[user].push(EnergyRecord(kWh, block.timestamp, signatureHash));
        
        emit MJMinted(user, mJAmount);
        emit EnergyRecorded(user, kWh, block.timestamp);
    }
    
    function processCarbonCredits(address user) external onlyOwner {
        uint256 pending = pendingCarbonCredits[user];
        require(pending > 0, "No pending credits");
        
        uint256 tokenId = aCTotalSupply;
        _mint(user, tokenId);
        
        carbonCredits[tokenId] = CarbonCredit({
            kgCO2: pending,
            vintage: block.timestamp,
            methodology: "SA Grid Displacement",
            deviceId: bytes32(0),
            retired: false
        });
        
        pendingCarbonCredits[user] = 0;
        aCTotalSupply++;
        
        emit ACMinted(user, tokenId, pending);
    }
    
    function burnMJ(uint256 amount) external {
        require(mJBalanceOf[msg.sender] >= amount, "Insufficient mJ balance");
        mJBalanceOf[msg.sender] -= amount;
        mJTotalSupply -= amount;
    }
    
    function retireAC(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        require(!carbonCredits[tokenId].retired, "Already retired");
        
        carbonCredits[tokenId].retired = true;
        _burn(tokenId);
        
        emit TokenRetired(msg.sender, tokenId, carbonCredits[tokenId].kgCO2, 
            string(abi.encodePacked("CERT-", uint2str(tokenId))));
    }
    
    function setCarbonPrice(int256 _price) external onlyOwner {
        latestCarbonPrice = _price;
        emit CarbonPriceUpdated(_price);
    }
    
    function setElectricityTariff(uint256 _tariff) external onlyOwner {
        electricityTariff = _tariff;
        emit ElectricityTariffUpdated(_tariff);
    }
}
```

**Deployed Address (Amoy):** `0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe`

### 4.2 Governor.sol

DAO governance for aC token holders.

```solidity
// Simplified - uses OpenZeppelin Governor
contract UmbaneGovernor is Governor, ERC20Votes {
    
    uint256 public votingDelay = 1 days;
    uint256 public votingPeriod = 7 days;
    uint256 public proposalThreshold = 100e18; // 100 aC
    uint256 public quorum = 40e18; // 40% of supply
    
    function propose(address[] memory targets, uint256[] memory values, 
        bytes[] memory calldatas, string memory description) override returns (uint256) {
        // Standard Governor proposal
    }
    
    function castVote(uint256 proposalId, uint8 support) override returns (uint256) {
        // Standard Governor vote
    }
}
```

### 4.3 Bridge.sol

Bridge contracts for COAS/JSE integration.

```solidity
contract Bridge {
    
    uint256 public bridgeFeePercent = 5; // 5%
    uint256 public verificationFee = 50e18; // R50/ton
    
    function bridgeToCOAS(uint256[] memory tokenIds) external {
        // 1. Burn aC NFTs
        // 2. Generate Merkle proof
        // 3. Emit BridgeToCOAS event
        // 4. User submits to COAS manually
    }
}
```

---

## 5. Backend API Specifications

### 5.1 Base URL
```
Development: http://localhost:8000
Production: https://api.umbane.co.za (planned)
```

### 5.2 Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Authenticate user, return JWT |

#### Device Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/device/register` | Register new ESP32 device |
| GET | `/api/v1/device/{device_id}` | Get device info |
| GET | `/api/v1/device/{device_id}/status` | Get device status |

#### Energy Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/energy/submit` | Submit signed energy data |
| GET | `/api/v1/energy/{device_id}/daily` | Daily production |
| GET | `/api/v1/energy/{device_id}/history` | Historical data |
| GET | `/api/v1/energy/aggregate` | Aggregated system stats |

#### Token Operations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/user/{address}/balance` | Token balances |
| GET | `/api/v1/user/{address}/history` | Transaction history |
| POST | `/api/v1/token/mint` | Manual mint (owner only) |
| POST | `/api/v1/token/burn` | Burn tokens |

#### Pricing
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/carbon/price` | Multi-source price feed |
| GET | `/api/v1/carbon/price/history` | Historical prices |

#### Electricity
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/electricity/tariff` | Current tariff |
| POST | `/api/v1/electricity/purchase` | Purchase electricity |

#### Bridge
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/bridge/to-coas` | Bridge to COAS registry |

### 5.3 Data Formats

**Energy Submission:**
```json
POST /api/v1/energy/submit
{
  "device_id": "0x8a3f92b1",
  "timestamp": 1711238400,
  "voltage": 230.5,
  "current": 12.3,
  "power": 2834,
  "energy_kwh": 2.45,
  "frequency": 50.1,
  "power_factor": 0.98,
  "signature": "0x3045022100a1b2c3..."
}
```

**Price Response:**
```json
{
  "price_zar": 178.50,
  "price_usd": 9.92,
  "volume_24h": 50000,
  "liquidity_tvl": 875000,
  "sources": {
    "uniswap": 180.00,
    "jse_feed": 175.00,
    "xpansiv": 177.00,
    "twap_24h": 178.25
  },
  "timestamp": "2026-03-20T14:35:00Z"
}
```

---

## 6. Frontend Specifications

### 6.1 Pages/Components

| Page | Route | Description |
|------|-------|-------------|
| Dashboard | `/` | Main dashboard with energy stats |
| Wallet | `/wallet` | Token balances, transactions |
| Trading | `/trade` | DEX integration, swap interface |
| Retirement | `/retire` | Carbon token retirement |
| Grid Purchase | `/electricity` | Buy electricity with tokens |
| DAO | `/governance` | Proposal voting |
| Devices | `/devices` | Device management |

### 6.2 Wallet Connection

```javascript
// Connect to MetaMask
const connectWallet = async () => {
  if (window.ethereum) {
    const accounts = await window.ethereum.request({
      method: 'eth_requestAccounts'
    });
    return accounts[0];
  }
  throw new Error("No wallet found");
}

// Switch to Polygon Amoy
const switchNetwork = async () => {
  await window.ethereum.request({
    method: 'wallet_switchEthereumChain',
    params: [{ chainId: '0x13882' }] // Amoy chain ID
  });
}
```

### 6.3 Contract Interaction

```javascript
// Token ABI (simplified)
const TOKEN_ABI = [
  "function mJBalanceOf(address) view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
  "function ownerOf(uint256) view returns (address)",
  "function burnMJ(uint256) external",
  "function retireAC(uint256) external"
];

// Contract address
const TOKEN_ADDRESS = "0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe";
```

---

## 7. Hardware Specifications

### 7.1 ESP32 Device

**Pin Configuration:**
```
PZEM-004T → ESP32
-----------------
VCC (Red)   → 5V (or 3.3V depending on module)
GND (Black) → GND
TX (Yellow) → GPIO16 (RX2)
RX (White)  → GPIO17 (TX2)

CT Clamp (SCT-013) → PZEM-004T
--------------------------------
S1 (White)  → T1 (input)
S2 (Red)    → T2 (output)
```

### 7.2 Data Packet

```c
// ESP32 Firmware - Data Structure
struct EnergyData {
    uint32_t timestamp;      // Unix epoch
    float voltage;           // V
    float current;           // A
    float power;             // W
    float energy_kwh;        // kWh
    float frequency;         // Hz
    float power_factor;      // 0.0-1.0
    uint8_t device_id[8];    // Unique ID
};

// Signing
void sign_data(EnergyData* data, uint8_t* signature) {
    // ECDSA sign using secp256k1
    // Private key stored in secure flash
}
```

### 7.3 Transmission

- **Protocol:** MQTT or HTTP POST
- **Frequency:** Every 15 minutes or on significant change
- **Encryption:** TLS for HTTP, or LoRa with AES-128

---

## 8. Security Considerations

### 8.1 Device Authentication
- ECDSA secp256k1 signatures on all data packets
- Public key registered on backend before deployment
- Replay protection via timestamp validation (±24 hours)

### 8.2 Smart Contract Security
- Ownable for admin functions (mint, price setting)
- Reentrancy guards on critical functions
- pausable in case of emergency

### 8.3 Frontend Security
- Wallet connection via injected provider (MetaMask)
- No private keys stored in frontend
- Input validation on all forms

### 8.4 Backend Security
- JWT authentication for protected endpoints
- Rate limiting on submission endpoints
- Database encryption at rest

---

## 9. Deployment

### 9.1 Networks

| Network | Chain ID | RPC URL | Status |
|---------|----------|---------|--------|
| Polygon Amoy | 80002 | `https://rpc-amoy.polygon.technology` | Active |
| Polygon Mainnet | 137 | `https://polygon-rpc.com` | Future |

### 9.2 Environment Variables

**Backend (.env):**
```
DATABASE_URL=postgresql://...
JWT_SECRET=...
POLYGON_RPC_URL=https://rpc-amoy.polygon.technology
TOKEN_CONTRACT_ADDRESS=0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe
ORACLE_PRIVATE_KEY=...
```

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TOKEN_ADDRESS=0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe
REACT_APP_CHAIN_ID=80002
```

---

## 10. Testing

### 10.1 Smart Contract Tests
```bash
cd contract-merge
forge test
```

### 10.2 API Tests
```bash
cd backend
pytest
```

### 10.3 Frontend Tests
```bash
cd frontend
npm test
```

---

## 11. Milestones

| Phase | Description | Target |
|-------|-------------|--------|
| Phase 1 | MVP - Basic token minting | Month 1-3 |
| Phase 2 | Beta - DEX integration, 100 devices | Month 4-6 |
| Phase 3 | Launch - Full features, 1,000+ devices | Month 7-12 |

---

**Document Author:** Umbane Development Team  
**Last Updated:** March 27, 2026