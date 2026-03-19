# Umbane Tokenized On-Chain Carbon/Energy System

## Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** March 19, 2026  
**Status:** Draft  

---

## 1. Executive Summary

Umbane is a **tokenized on-chain carbon and energy system** that enables prosumers (households with solar installations) to monetize their clean energy production as verifiable carbon credits and tradeable tokens.

The system acquires energy data via **CT clamp sensors** connected to **ESP32 microcontrollers**, which transmit signed measurements to an **ESP "Oracle"** that verifies and submits data to the **Polygon blockchain**. The smart contract issues users with **UMB tokens** representing their energy production and carbon offset value.

UMB tokens serve multiple purposes:
- **Trading**: Exchanged for stablecoins via Carbon Trading Desks
- **Retirement**: Permanently retired to claim carbon offset value
- **Storage**: Held as "Tokenised Energy" reserves for future use
- **Pledging**: Donated/pay-forward to households without solar access

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

| Component | Description | Technology |
|-----------|-------------|------------|
| **CT Clamp Sensor** | Non-invasive current sensor on solar feed-in line | SCT-013-030 (30A) or SCT-013-100 (100A) |
| **ESP32 Device** | Microcontroller that measures, calculates, and signs energy data | ESP32-WROOM-32 or TTGO T-Beam |
| **ESP Oracle** | Backend service that verifies signed data and submits to chain | Python/FastAPI |
| **Smart Contract** | Polygon-based token contract that mints UMB tokens | Solidity (ERC20) |
| **Frontend Dashboard** | User interface for viewing energy production and token balances | React/JavaScript |
| **Carbon Trading Desk** | DEX integration for swapping UMB for stablecoins | QuickSwap/SushiSwap |
| **Oracle System** | Off-chain verification layer ensuring data integrity | Chainlink-style |

---

## 3. Token Specification

### 3.1 Token Overview

| Token | Symbol | Description | Standard |
|-------|--------|-------------|----------|
| **Umbane Energy** | **mJ** | Represents energy produced (millijoules) | ERC20 |
| **Umbane Carbon** | **aC** | Represents carbon offset (kg CO2) | ERC20 |

### 3.2 Token Mechanics

#### 3.2.1 mJ (Millijoules - Energy Token)

- **Minting**: 1 mJ minted per Wh (watt-hour) of verified solar feed-in
- **Purpose**: Represents the energy value of solar production
- **Use Cases**:
  - Held as "Tokenised Energy" for future consumption
  - Traded on Carbon Trading Desks
  - Used in community energy sharing

#### 3.2.2 aC (Carbon Credits)

- **Minting**: Calculated from energy production using emission factor
  - South Africa grid: 0.5 kg CO2/kWh (Eskom)
  - 1 kWh solar = 500g CO2 offset = 500 aC
- **Purpose**: Represents verified carbon offset value
- **Use Cases**:
  - Retired to claim carbon offset (permanent)
  - Traded on carbon markets
  - Pledged to community fund

### 3.3 Conversion Rates

```
Energy to Carbon Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1 kWh (1000 Wh) = 1000 mJ (energy token)
1 kWh = 500g CO2 offset = 500 aC (carbon token)

Emission Factor: 0.5 kg CO2/kWh (South Africa grid average)
```

---

## 4. Functional Requirements

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

### 6.1 Smart Contract (Token.sol)

#### 6.1.1 Contract State Variables

```solidity
uint256 public mJTotalSupply;      // Total mJ tokens minted
uint256 public aCTotalSupply;      // Total aC tokens minted
int256 public latestCarbonPrice;  // Current carbon price (USD/kg)
uint256 public latestCarbonPriceTimestamp;

mapping(address => UserEnergyRecord[]) public userEnergyHistory;
mapping(address => uint256) public pendingCarbonCredits;
```

#### 6.1.2 Key Functions

| Function | Description | Access |
|----------|-------------|--------|
| `recordEnergyUsage(address user, uint256 energyUsed)` | Called by Oracle to record energy and mint tokens | Oracle only |
| `processEnergyRecord(address user)` | Finalizes pending aC tokens after verification | Oracle only |
| `mintMJ(address to, uint256 amount)` | Mints energy tokens | Owner only |
| `mintAC(address to, uint256 amount)` | Mints carbon tokens | Owner only |
| `burnMJ(uint256 amount)` | Burns mJ tokens (spending/retirement) | Public |
| `burnAC(uint256 amount)` | Burns aC tokens (retirement only) | Public |
| `setCarbonPrice(int256 _price)` | Updates carbon price feed | Owner only |

#### 6.1.3 Events

```solidity
event MJMinted(address indexed to, uint256 amount);
event ACMinted(address indexed to, uint256 amount);
event CarbonPriceUpdated(int256 price);
event EnergyRecorded(address indexed user, uint256 kWh, uint256 timestamp);
event TokenRetired(address indexed user, uint256 amount, string certificateId);
event TokenPledged(address indexed from, address indexed to, uint256 amount);
```

### 6.2 ESP Oracle (Backend)

#### 6.2.1 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/energy/submit` | POST | Accept signed energy data from devices |
| `/api/v1/energy/{device_id}/daily` | GET | Get daily production for device |
| `/api/v1/oracle/batch-submit` | POST | Internal: submit batch to smart contract |
| `/api/v1/user/{address}/balance` | GET | Get user's token balances |
| `/api/v1/user/{address}/history` | GET | Get user's energy history |
| `/api/v1/carbon/price` | GET | Get current carbon price |

#### 6.2.2 Oracle Workflow

```
1. RECEIVE   ← Signed data packet from ESP32 device
2. VERIFY    ← Check signature matches registered device
3. DEDUP     ← Reject duplicate timestamps (replay protection)
4. VALIDATE  ← Check timestamp within ±24 hours
5. STORE     ← Persist to PostgreSQL with verified=true
6. BATCH     ← Aggregate multiple submissions (10-50 per tx)
7. SUBMIT    ← Call smart contract recordEnergyUsage()
8. CONFIRM   ← Log transaction hash for audit trail
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
- **Quick Actions**: Trade, Retire, Pledge buttons

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
| **ESP Oracle** | Backend service that verifies device data and submits to blockchain |
| **mJ Token** | Umbane Energy token - represents energy produced (millijoules) |
| **aC Token** | Umbane Carbon token - represents carbon offset (kg CO2) |
| **Prosumer** | Consumer who also produces energy (solar panel owner) |
| **DEX** | Decentralized Exchange - automated token trading protocol |
| **Retirement** | Permanent removal of carbon tokens from circulation (claiming offset) |
| **Pledging** | Donating tokens to community pool for redistribution |

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
| South Africa | 0.50 | Eskom 2024 |
| EU | 0.28 | EEA 2024 |
| USA (average) | 0.42 | EPA 2024 |
| China | 0.58 | MIIT 2024 |
| World Average | 0.50 | IEA 2024 |

---

**Document Author:** Umbane Development Team  
**Last Updated:** March 19, 2026  
**Next Review:** After Phase 1 MVP deployment
