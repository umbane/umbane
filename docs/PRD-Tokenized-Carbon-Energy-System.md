# Umbane Tokenized On-Chain Carbon/Energy System

## Product Requirements Document (PRD)

**Version:** 1.2  
**Date:** March 27, 2026  
**Status:** Draft  
**Based on:** umbane_carbon_market_discussion_paper.txt  

---

## 1. Executive Summary

Umbane is a **tokenized on-chain carbon and energy system** that enables prosumers (households with solar installations) to monetize their clean energy production as verifiable carbon credits and tradeable tokens.

The system acquires energy data via **CT clamp sensors** connected to **ESP32 microcontrollers** with **PZEM-004T voltage/power measurement module**, which transmit signed measurements to an **ESP "Oracle"** that verifies and submits data to the **Polygon blockchain**. The smart contract issues users with **mJ and aC tokens** representing their energy production and carbon offset value.

### 2.1 South African Market Context

South Africa's carbon and energy certificate market operates under multiple overlapping frameworks with significant barriers for small-scale producers:

**Registration Barriers (as of 2026):**
- **zaREC (Pty) Ltd**: R25,000/device registration fee (ex VAT), minimum transaction fee ~R4,600 (ex VAT)
- **I-REC (GCC)**: £800-2,500/device registration fee, administered from Sheffield, UK
- These costs immediately exclude household solar prosumers and township microgrids

**Key Market Players:**
| Entity | Role | Notes |
|--------|------|-------|
| **zaREC (Pty) Ltd** | Local REC registry | 12 active market makers, 179 organizational buyers |
| **RECSA** | Industry body | Non-profit supporting SA REC market |
| **GCC** | I-REC Central Issuer | UK-based, sole SA issuer |
| **COAS** | Carbon Offset Registry | Tax-eligible offsets for carbon tax compliance |
| **JSE Ventures** | Carbon Trading | White-label Xpansiv CBL, not a market maker |
| **Xpansiv/Evident** | Infrastructure | Single-vendor dependency, no public API |

**Pricing (JSE Ventures - spot):**
- Generic VCU (Verra): R120-R180/ton CO2 ($7-$10 USD)
- I-REC (SA wind/solar): R8-R15/MWh ($0.44-$0.83 USD)
- Volatility: ±40% within 90 days (no transparent benchmark)

**Umbane's Solution:** Create a parallel tokenized system that aggregates I-REC/zaREC registration for domestic-scale producers, bypassing the R25,000/device barrier while maintaining optional bridges to traditional registries (COAS, JSE) via verifiable oracles.

UMB tokens serve multiple purposes:
- **Trading**: Exchanged for stablecoins via Carbon Trading Desks
- **Retirement**: Permanently retired to claim carbon offset value
- **Storage**: Held as "Tokenised Energy" reserves for future use
- **Pledging**: Donated/pay-forward to households without solar access
- **Grid Purchase**: Exchanged for electricity credits from the municipal grid

---

## 2. System Architecture

### 2.1 High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         UMBANE SYSTEM ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  CT CLAMP    │────▶│    ESP32     │────▶│   ESP        │
  │  SENSOR      │     │  MICROCONTROL│     │   ORACLE     │
  │  (Feed-in)   │     │              │     │   (Backend)  │
  └──────────────┘     └──────────────┘     └──────┬───────┘
                                                    │
                                                    │ Signed Data
                                                    ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                     POLYGON BLOCKCHAIN                           │
  │  ┌─────────────────┐    ┌─────────────────┐                     │
  │  │   Token.sol    │    │   Oracle.sol    │                     │
  │  │   (UMB Token)  │    │   (Verifier)   │                     │
  │  └────────┬────────┘    └────────┬────────┘                     │
  │           │                     │                               │
  │           ▼                     │                               │
  │  ┌─────────────────────────────┴───────────┐                  │
  │  │          UMB TOKEN MINTING                │                  │
  │  │  - mJ (millijoules - energy)              │                  │
  │  │  - aC (carbon credits)                    │                  │
  │  └───────────────────────────────────────────┘                  │
  └──────────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                      USER INTERFACES                             │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
  │  │  WEB/APP    │  │  TRADING   │  │   COMMUNITY/DAO        │  │
  │  │  DASHBOARD  │  │  DESK      │  │   GOVERNANCE           │  │
  │  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

| Component | Description | Technology | Cost (ZAR) |
|-----------|-------------|------------|------------|
| **CT Clamp Sensor** | Non-invasive current sensor on solar feed-in line | SCT-013-030 (30A) or SCT-013-100 (100A) | R200-R500 |
| **PZEM-004T Module** | Voltage, current, power, frequency, power factor measurement | AC voltage: 80-260V, Current: 0-100A | R150-R300 |
| **ESP32 Device** | Microcontroller that measures, calculates, and signs energy data | ESP32-WROOM-32 or TTGO T-Beam | R250-R500 |
| **LoRa Module** | Long-range wireless communication | Ra-01 SX1278 or built-in | R100-R200 |
| **ESP Oracle** | Backend service that verifies signed data and submits to chain | Python/FastAPI | - |
| **Smart Contract** | Polygon-based token contract that mints tokens | Solidity (ERC20/ERC721) | - |
| **Frontend Dashboard** | User interface for viewing energy production and token balances | React/JavaScript | - |
| **Carbon Trading Desk** | DEX integration for swapping tokens for stablecoins | QuickSwap/SushiSwap | - |
| **Oracle System** | Off-chain verification layer ensuring data integrity | Chainlink-style | - |

---

## 3. Token Specification

### 3.1 Token Overview

| Token | Symbol | Description | Standard | Implementation |
|-------|--------|-------------|----------|----------------|
| **Umbane Energy** | **mJ** | Represents energy produced (millijoules) | ERC-20 | ✓ Implemented as ERC-20 |
| **Umbane Carbon** | **aC** | Represents carbon offset (kg CO2) | ERC-20 | ✓ Implemented as ERC-20 (NOT NFT) |

**Note:** The PRD originally specified aC as ERC-721 NFT, but the actual implementation uses ERC-20 for both tokens (Option C). This was simpler for DeFi integration.

### 3.2 Token Mechanics

#### 3.2.1 mJ (Millijoules - Energy Token)

- **Minting**: 1 mJ minted per Wh (watt-hour) of verified solar feed-in
- **Accumulator**: Smart contract treats incoming data as "drops" (millijoules) and only mints a tradeable 1 Wh token once total reaches 3,600,000 mJ (1 kWh)
- **Purpose**: Represents the energy value of solar production
- **Use Cases**:
  - Held as "Tokenised Energy" for future consumption
  - Traded on Carbon Trading Desks
  - Used in community energy sharing
  - Burned for grid electricity purchase

#### 3.2.2 aC (Carbon Credits - NFT)

- **Type**: ERC-721 NFT with metadata (project_id, vintage, emission_factor, device_id, production_period)
- **Minting**: Calculated from energy production using emission factor
  - South Africa grid (2026): 0.9 kg CO2/kWh
  - 1 kWh solar = 900 g CO2 offset = 0.9 aC
- **Conversion Formula**: `aC (kg CO2) = mJ tokens / 1,000,000 × Emission Factor`
- **Purpose**: Represents verified carbon offset value as unique NFT
- **Use Cases**:
  - Retired to claim carbon offset (permanent)
  - Traded on carbon markets (peer-to-peer or via liquidity pool)
  - Used for DAO governance (1 aC = 1 vote)
  - Pledged to community fund

### 3.3 Conversion Rates

```
Energy to Carbon Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1 kWh (1000 Wh) = 1,000,000 mJ (energy token)
1 kWh = 0.9 kg CO2 offset = 0.9 aC (carbon NFT)

Emission Factor: 0.9 kg CO2/kWh (South Africa grid - 2026 update)

Example:
10,000 kWh solar production
= 10,000,000 mJ tokens
= 10,000 kWh × 0.9 kg CO2/kWh
= 9,000 kg CO2 offset
= 9 aC NFTs (assuming 1 NFT = 1 ton CO2)
```

**Pricing Mechanisms:**

1. **Primary Market (Newly Minted aC)**:
   - Algorithmic floor price: Max(JSE carbon spot × 0.8, R100/ton)
   - Example: If JSE VCU = R150, floor = R120/ton
   - Minting cost: R50/aC (covers oracle + tx costs)
   - Prosumer receives: R120 - R50 = R70 net per ton

2. **Secondary Market (aC Trading)**:
   - DeFi Pool: aC/USDC on Uniswap (market price)
   - P2P: Direct wallet-to-wallet trades
   - Marketplace: Umbane marketplace with offers/bids
   - Price discovery via: AMM curve + arbitrage

3. **Bridge Price (aC → COAS)**:
   - Bridge fee: 5% of off-chain value
   - Example: aC = R120, COAS credit = R180 → bridge fee = R9
Energy to Carbon Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1 kWh (1000 Wh) = 1000 mJ (energy token)
1 kWh = 500g CO2 offset = 500 aC (carbon token)

Emission Factor: 0.5 kg CO2/kWh (South Africa grid average)

Grid Purchase Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Token Price = Grid Tariff (ZAR/kWh)
Example: R2.50/kWh → 1000 mJ = R2.50
To purchase 50 kWh: 50,000 mJ tokens burned
```

---

## 4. Functional Requirements

### 4.0 DAO Governance (FR-GOV)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-GOV-01 | aC token holders must have voting rights in DAO | Must |
| FR-GOV-02 | 1 aC token staked = 1 vote in DAO | Must |
| FR-GOV-03 | Voting on: carbon price parameters, device verification standards, treasury allocation, protocol upgrades | Must |
| FR-GOV-04 | Proposal creation: any aC holder with >100 aC can propose | Should |
| FR-GOV-05 | Proposal threshold: 51% for standard, 67% for protocol upgrades | Must |
| FR-GOV-06 | Quorum: 4% of total aC staked required for proposal to pass | Must |

### 4.1 Data Acquisition (FR-DA)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-DA-01 | System must measure electrical current on solar feed-in line using CT clamp sensor | Must |
| FR-DA-02 | System must calculate power (W) and energy (kWh) from current measurements | Must |
| FR-DA-03 | Device must timestamp each reading with Unix epoch | Must |
| FR-DA-04 | Device must sign all data packets with ECDSA (secp256k1) before transmission | Must |
| FR-DA-05 | System must aggregate readings at minimum 15-minute intervals | Must |
| FR-DA-06 | Device must transmit data via LoRaWAN or WiFi | Should |
| FR-DA-07 | System must detect and flag anomalous readings (>10kW residential) | Should |

### 4.2 Oracle Verification (FR-OR)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-OR-01 | Oracle must verify device signature before accepting data | Must |
| FR-OR-02 | Oracle must reject duplicate submissions (replay attack prevention) | Must |
| FR-OR-03 | Oracle must validate timestamp is within acceptable window (±24 hours) | Must |
| FR-OR-04 | Oracle must batch multiple device submissions for gas efficiency | Should |
| FR-OR-05 | Oracle must submit verified data to smart contract within 1 hour of receipt | Should |

### 4.3 Token Minting (FR-TM)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-TM-01 | Smart contract must mint mJ tokens upon verified energy submission | Must |
| FR-TM-02 | Smart contract must calculate and queue aC tokens (pending verification) | Must |
| FR-TM-03 | Smart contract must store complete energy history per user | Must |
| FR-TM-04 | Users must be able to view pending carbon credits before minting | Must |
| FR-TM-05 | Smart contract must emit events for all minting operations | Should |

### 4.4 Token Trading (FR-TT)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-TT-01 | Users must be able to swap UMB tokens for stablecoins (USDC/USDT) | Must |
| FR-TT-02 | System must integrate with DEX liquidity pools (QuickSwap) | Must |
| FR-TT-03 | Trading desk must display real-time price feeds | Must |
| FR-TT-04 | System must support limit orders and market orders | Should |
| FR-TT-05 | Transaction fees must be split between protocol and liquidity providers | Must |

### 4.5 Token Retirement (FR-TR)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-TR-01 | Users must be able to permanently retire aC tokens | Must |
| FR-TR-02 | Retirement must generate verifiable carbon offset certificate | Must |
| FR-TR-03 | Retired tokens must be burned and cannot be transferred | Must |
| FR-TR-04 | System must record retirement on-chain with timestamp and beneficiary | Must |

### 4.6 Tokenised Energy Storage (FR-ES)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-ES-01 | Users must be able to hold mJ tokens as energy reserves | Must |
| FR-ES-02 | Energy reserves must be withdrawable as grid credit (future) | Should |
| FR-ES-03 | System must display "energy wallet" balance in kWh equivalent | Must |

### 4.7 Pledging/Pay-Forward (FR-PF)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-PF-01 | Users must be able to pledge/donate tokens to community pool | Must |
| FR-PF-02 | Pledged tokens must be tracked separately from spendable balance | Must |
| FR-PF-03 | Community pool must be governed by DAO (token-weighted voting) | Should |
| FR-PF-04 | Recipients must be able to claim from pool (KYC verification) | Should |

### 4.8 Grid Electricity Purchase (FR-GP)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-GP-01 | Users must be able to purchase electricity from the municipal grid using mJ tokens | Must |
| FR-GP-02 | System must convert mJ tokens to grid credit at current tariff rate | Must |
| FR-GP-03 | System must integrate with City of Cape Town prepaid meter API | Must |
| FR-GP-04 | Grid purchase must burn mJ tokens upon successful transaction | Must |
| FR-GP-05 | System must record purchase on-chain with timestamp and kWh value | Must |
| FR-GP-06 | User must receive confirmation with meter number and kWh purchased | Must |
| FR-GP-07 | System must support both full token payment and token+cash hybrid payments | Should |

---

## 5. User Stories

### 5.1 Prosumer (Solar Producer)

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-P-01 | As a prosumer, I want my solar feed-in to be automatically measured so I can earn tokens | CT clamp captures data; ESP signs and transmits; Oracle verifies and submits to chain |
| US-P-02 | As a prosumer, I want to view my energy production history so I can track my impact | Dashboard displays daily/weekly/monthly charts with kWh and token values |
| US-P-03 | As a prosumer, I want to trade my tokens for stablecoins so I can monetize my energy | Trading desk allows swap with <2% slippage for amounts <$1000 |
| US-P-04 | As a prosumer, I want to retire my carbon tokens so I can claim my environmental impact | One-click retirement generates certificate with serial number |
| US-P-05 | As a prosumer, I want to keep my tokens as energy savings for a rainy day | Balance displayed in kWh equivalent with projected grid value |
| US-P-06 | As a prosumer, I want to purchase electricity from the grid using my tokens so I don't need cash | Enter kWh amount, confirm tokens burned, receive electricity credit on meter |

### 5.2 Carbon Trading Desk Operator

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-T-01 | As a trader, I want to buy UMB tokens so I can speculate on carbon prices | Order book shows bids/asks; instant execution for market orders |
| US-T-02 | As a trader, I want to provide liquidity so I can earn fees | Liquidity pools show APY; one-click add/remove liquidity |
| US-T-03 | As a trader, I want real-time price feeds so I can make informed decisions | Price ticker updates every 30 seconds; historical charts available |

### 5.3 Community Member (Non-Solar)

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-C-01 | As a community member without solar, I want to receive pledged energy so I can reduce my bills | Application form submits to DAO; approved claims receive token transfer |
| US-C-02 | As a community member, I want to vote on how community tokens are distributed | DAO governance interface shows proposals; one token = one vote |

---

## 6. Technical Specifications

### 6.1 Smart Contracts (Polygon)

#### 6.1.1 Contract Overview

| Contract | Purpose | Standard |
|----------|---------|----------|
| **Token.sol** | mJ (ERC-20) and aC (ERC-721) token issuance | ERC-20 + ERC-721 |
| **Governor.sol** | DAO governance for aC holders | OpenZeppelin Governor |
| **Oracle.sol** | Chainlink integration for price feeds | Chainlink VRF |
| **Marketplace.sol** | P2P aC trading with order matching | Custom |
| **Bridge.sol** | Bridge to COAS/JSE off-chain registries | Custom |

#### 6.1.2 Token.sol State Variables

```solidity
// ERC-20 mJ Token
uint256 public mJTotalSupply;      // Total mJ tokens minted
mapping(address => uint256) public mJBalanceOf;

// ERC-721 aC Token (NFT)
uint256 public aCTotalSupply;      // Total aC tokens minted
struct CarbonCredit {
    uint256 tokenId;
    address owner;
    uint256 kgCO2;                 // Offset amount
    uint256 vintage;               // Year minted
    string methodology;            // Carbon methodology
    bytes32 deviceId;             // Source device
    uint256 timestamp;
    bool retired;
}
mapping(uint256 => CarbonCredit) public carbonCredits;

// Pricing
int256 public latestCarbonPrice;  // Current carbon price (USD/kg)
uint256 public electricityTariff;  // Current tariff (ZAR/kWh)
uint256 public latestCarbonPriceTimestamp;

// User Data
mapping(address => EnergyRecord[]) public userEnergyHistory;
mapping(address => uint256) public pendingCarbonCredits;
```

#### 6.1.3 Key Functions

| Function | Description | Access |
|----------|-------------|--------|
| `recordEnergyUsage(address user, uint256 energyUsed)` | Called by Oracle to record energy and mint mJ tokens | Oracle only |
| `processEnergyRecord(address user)` | Finalizes pending aC tokens after verification | Oracle only |
| `mintMJ(address to, uint256 amount)` | Mints energy tokens | Owner only |
| `mintAC(address to, uint256 amount)` | Mints carbon tokens (NFT) | Owner only |
| `burnMJ(uint256 amount)` | Burns mJ tokens (spending/retirement/grid purchase) | Public |
| `burnAC(uint256 amount)` | Burns aC tokens (retirement only) | Public |
| `retireAC(uint256 tokenId)` | Permanently retires carbon NFT, emits certificate | Public |
| `setCarbonPrice(int256 _price)` | Updates carbon price feed | Owner only |
| `setElectricityTariff(uint256 _tariff)` | Sets current electricity tariff (ZAR/kWh) | Owner only |
| `purchaseElectricity(address user, uint256 kwhAmount)` | Burns mJ tokens and records electricity purchase | Oracle only |
| `getElectricityTariff()` | Returns current tariff rate | Public |

#### 6.1.4 Events

```solidity
event MJMinted(address indexed to, uint256 amount);
event ACMinted(address indexed to, uint256 tokenId, uint256 kgCO2);
event CarbonPriceUpdated(int256 price);
event EnergyRecorded(address indexed user, uint256 kWh, uint256 timestamp);
event TokenRetired(address indexed user, uint256 tokenId, uint256 kgCO2, string certificateId);
event TokenPledged(address indexed from, address indexed to, uint256 amount);
event ElectricityPurchased(address indexed user, uint256 kwhAmount, uint256 tokensBurned, string meterNumber);
event ElectricityTariffUpdated(uint256 newTariff);
event BridgeToCOAS(address indexed user, uint256[] tokenIds, bytes32 merkleRoot);
```

### 6.2 ESP Oracle (Backend)

#### 6.2.1 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/device/register` | POST | Register new ESP32 device with public key |
| `/api/v1/energy/submit` | POST | Accept signed energy data from devices |
| `/api/v1/energy/{device_id}/daily` | GET | Get daily production for device |
| `/api/v1/energy/{device_id}/history` | GET | Get historical production data |
| `/api/v1/oracle/batch-submit` | POST | Internal: submit batch to smart contract |
| `/api/v1/user/{address}/balance` | GET | Get user's token balances |
| `/api/v1/user/{address}/history` | GET | Get user's energy history |
| `/api/v1/carbon/price` | GET | Get current carbon price (multi-source) |
| `/api/v1/electricity/purchase` | POST | Purchase grid electricity using tokens |
| `/api/v1/electricity/tariff` | GET | Get current electricity tariff rate |
| `/api/v1/bridge/to-coas` | POST | Bridge aC tokens to COAS registry |

#### 6.2.2 Oracle Workflow

```
1. RECEIVE   ← Signed data packet from ESP32 device
2. VERIFY    ← Check signature matches registered device public key
3. DEDUP     ← Reject duplicate timestamps (replay protection)
4. VALIDATE  ← Check timestamp within ±24 hours
5. ORACLE    ← Cross-reference with Chainlink oracle (solar irradiance data)
6. STORE     ← Persist to PostgreSQL with verified=true
7. BATCH     ← Aggregate multiple submissions (10-50 per tx)
8. SUBMIT    ← Call smart contract recordEnergyUsage()
9. MINT      ← Smart contract mints mJ (immediate) and queues aC (pending verification)
10. CONFIRM  ← Log transaction hash for audit trail
```

#### 6.2.3 Device Registration Flow (I-REC/zaREC Aggregation)

The system supports two registration paths:

**Path A: Direct Device Registration (Umbane Native)**
- Device registers directly with Umbane (R500 one-time onboarding)
- Low-cost IoT devices (R1,200-R2,100) with tamper-proof ECDSA signing
- Suitable for household solar prosumers excluded by traditional registries

**Path B: Aggregated I-REC/zaREC Registration**
- Umbane acts as third-party registrant for multiple devices
- Reduces per-device cost through aggregation (I-REC explicitly allows this)
- Can batch-register 100-1,000 devices via CSV upload
- Free registrant enrollment; device fees still apply

**Registration Data Required:**
```json
{
  "device_id": "0x8a3f92b1",
  "public_key": "0x04a1b2c3...",
  "location": {
    "lat": -34.1050,
    "lon": 18.4750,
    "address": "Cape Town, South Africa"
  },
  "installation_capacity_kw": 5.2,
  "grid_connection": "Nedlink prepaid meter",
  "registration_path": "direct" | "irec_aggregated" | "zarec_aggregated"
}
```

### 6.3 Device Firmware (ESP32)

#### 6.3.1 Data Packet Structure

```json
{
  "device_id": "0x8a3f92b1",
  "timestamp": 1711238400,
  "voltage": 230.5,
  "current": 12.3,
  "power": 2834,
  "energy_kwh": 2.45,
  "frequency": 50.1,
  "power_factor": 0.98,
  "location": {
    "lat": -34.1050,
    "lon": 18.4750
  },
  "signature": "0x3045022100a1b2c3..."
}
```

#### 6.3.2 Measurement Schedule

- **Sample Rate**: 1 reading per second
- **Aggregate**: Every 15 minutes (900 readings)
- **Transmit**: Every 15 minutes OR batch hourly

---

## 7. Integration Requirements

### 7.1 Blockchain Networks

| Network | Chain ID | Status | Use Case |
|---------|----------|--------|----------|
| Polygon Amoy | 80002 | Primary | Development/Testing |
| Polygon Mainnet | 137 | Future | Production |

### 7.2 External Integrations

| Service | Integration | Purpose |
|---------|-------------|---------|
| **Chainlink** | Price Feeds | Carbon price oracle |
| **QuickSwap** | DEX | Token trading |
| **Polygon Scan** | Block Explorer | Transaction verification |
| **The Things Network** | LoRaWAN | Device connectivity |
| **City of Cape Town** | Prepaid Meter API | Electricity credit purchases |

---

## 8. Non-Functional Requirements

### 8.1 Performance

| Metric | Target |
|--------|--------|
| Data submission to oracle | < 5 seconds |
| Oracle verification | < 30 seconds |
| Smart contract confirmation | < 3 seconds (Polygon) |
| Dashboard load time | < 2 seconds |
| Token swap execution | < 10 seconds |

### 8.2 Security

| Requirement | Implementation |
|-------------|----------------|
| Device authentication | ECDSA signature verification |
| Replay attack prevention | Timestamp validation + nonce |
| Oracle authorization | Whitelisted address in smart contract |
| Frontend security | Wallet connection via MetaMask/WalletConnect |
| Key management | Hardware security module for Oracle signing keys |

### 8.3 Scalability

| Component | Target Capacity |
|-----------|-----------------|
| Devices supported | 10,000+ |
| Transactions per day | 100,000+ |
| Users supported | 50,000+ |

### 8.4 Availability

| Metric | Target |
|--------|--------|
| API uptime | 99.9% |
| Smart contract uptime | 100% (immutable) |
| Data retention | 7 years |

---

## 9. User Interface Requirements

### 9.1 Dashboard (Web/App)

#### 9.1.1 Prosumer Dashboard

- **Energy Production Widget**: Real-time kWh display with trend chart
- **Token Balance Widget**: mJ and aC balances with USD equivalent
- **History View**: Daily/weekly/monthly production tables
- **Quick Actions**: Trade, Retire, Pledge, Buy Electricity buttons
- **Grid Purchase Widget**: Quick buy electricity using token balance

#### 9.1.2 Token Management

- **Send/Receive**: Transfer tokens to other addresses
- **Swap Interface**: Integrated DEX for stablecoin exchange
- **Retire Flow**: One-click retirement with certificate download
- **Pledge Form**: Select recipient and amount for community giving

### 9.2 Carbon Trading Desk

- **Market Overview**: Token prices, volume, charts
- **Order Book**: Bids and asks for UMB pairs
- **Swap Interface**: Simple token-to-token exchange
- **Liquidity Pools**: Add/remove liquidity with APY display

### 9.3 Community/DAO Interface

- **Proposal List**: Active governance proposals
- **Voting Mechanism**: Token-weighted voting
- **Pool Statistics**: Total pledged, claimed, remaining

### 9.4 Grid Electricity Purchase Interface

- **Tariff Display**: Current electricity rate (ZAR/kWh)
- **Purchase Form**: Input kWh amount or ZAR value
- **Token Balance Check**: Shows mJ balance and equivalent kWh
- **Meter Number Input**: Enter prepaid meter number (for City of Cape Town)
- **Confirmation Dialog**: Shows token cost, kWh received, transaction fee
- **Purchase Receipt**: Digital receipt with transaction ID and meter confirmation

---

## 10. Testing Requirements

### 10.1 Test Scenarios

| ID | Scenario | Expected Result |
|----|----------|-----------------|
| T-01 | Valid signed data submission | Tokens minted, event emitted |
| T-02 | Invalid signature rejection | Transaction reverts with error |
| T-03 | Duplicate submission | Rejected with "already processed" |
| T-04 | Old timestamp rejection | Rejected with "timestamp expired" |
| T-05 | Token swap (mJ → USDC) | Tokens swapped at market rate |
| T-06 | Token retirement | Tokens burned, certificate generated |
| T-07 | Token pledge | Balance transferred to pool address |
| T-08 | DAO vote | Vote recorded, weight calculated |
| T-09 | Grid electricity purchase | mJ tokens burned, kWh credit recorded, meter updated |
| T-10 | Insufficient token balance for purchase | Transaction rejected with insufficient balance error |

### 10.2 Test Networks

- **Polygon Amoy**: Primary test network
- **Local Anvil**: Smart contract testing (Foundry)

---

## 11. Deployment Roadmap

### Phase 1: MVP (Months 1-3)

- [ ] CT clamp hardware prototype
- [ ] ESP32 firmware for data signing
- [ ] Backend oracle service
- [ ] Smart contract deployment (Amoy)
- [ ] Basic dashboard (view balances, history)
- [ ] Manual token minting for testing

### Phase 2: Beta (Months 4-6)

- [ ] Automated oracle submission
- [ ] Token trading integration (DEX)
- [ ] Mobile responsive dashboard
- [ ] User onboarding flow
- [ ] 100-device pilot deployment
- [ ] Grid electricity purchase integration

### Phase 3: Launch (Months 7-12)

- [ ] Full trading desk functionality
- [ ] Token retirement with certificates
- [ ] Pledging/community pool
- [ ] DAO governance
- [ ] Scale to 1,000+ devices
- [ ] Polygon Mainnet deployment

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **CT Clamp** | Current Transformer clamp - non-invasive sensor for measuring electrical current |
| **PZEM-004T** | Power measurement module measuring voltage, current, power, frequency, power factor |
| **ESP Oracle** | Backend service that verifies device data and submits to blockchain |
| **mJ Token** | Umbane Energy token (ERC-20) - represents energy produced (1 mJ = 1 Wh) |
| **aC Token** | Umbane Carbon token (ERC-721 NFT) - represents carbon offset |
| **Prosumer** | Consumer who also produces energy (solar panel owner) |
| **DEX** | Decentralized Exchange - automated token trading protocol |
| **Retirement** | Permanent removal of carbon tokens from circulation (claiming offset) |
| **Pledging** | Donating tokens to community pool for redistribution |
| **Grid Purchase** | Using mJ tokens to purchase electricity credit from municipal grid |
| **zaREC** | South African voluntary REC registry (R25,000/device registration) |
| **I-REC** | International Renewable Energy Certificate (GCC administered, UK-based) |
| **RECSA** | Renewable Energy Certificate South Africa - industry body |
| **COAS** | Carbon Offset Administration System - tax-eligible offsets |
| **GCC** | Green Certificate Company - I-REC central issuer for South Africa |
| **Xpansiv** | Infrastructure provider powering JSE Ventures Carbon Market |
| **AMM** | Automated Market Maker - algorithmic pricing via liquidity pools |
| **Emission Factor** | kg CO2 emitted per kWh of grid electricity (SA: 0.9 kg/kWh) |

---

## 13. Appendix

### A. Smart Contract Address (Amoy Testnet)

```
UMB Token (mJ): 0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe
```

### B. Carbon Calculation Formula

```python
def calculate_carbon_credits(energy_kwh: float, emission_factor: float = 0.5) -> float:
    """
    Calculate carbon offset from energy production
    
    Args:
        energy_kwh: Energy produced in kilowatt-hours
        emission_factor: kg CO2 per kWh (default: 0.5 for South Africa)
    
    Returns:
        Carbon offset in grams CO2
    """
    co2_kg = energy_kwh * emission_factor
    co2_grams = co2_kg * 1000
    return co2_grams
```

### C. Emission Factors by Region

| Region | Grid Emission Factor (kg CO2/kWh) | Source |
|--------|----------------------------------|--------|
| **South Africa** | **0.90** | Eskom 2026 (updated) |
| EU | 0.28 | EEA 2024 |
| USA (average) | 0.42 | EPA 2024 |
| China | 0.58 | MIIT 2024 |
| World Average | 0.50 | IEA 2024 |

---

**Document Author:** Umbane Development Team  
**Last Updated:** March 27, 2026  
**Next Review:** After Phase 1 MVP deployment
