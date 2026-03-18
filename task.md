# Umbane Development Tasks

## Priority 1: Foundation ✅ COMPLETE
- [x] Fix missing dependencies (backend/requirements.txt, frontend/package.json) → `bd: umbane-2mn`
- [x] Create database schema (users, transactions, tokens tables) → `bd: umbane-2dv`

## Priority 2: Backend API ✅ COMPLETE
- [x] Add remaining endpoints (mintAC, burnMJ, burnAC, getMJBalance, getACBalance) → `bd: umbane-7zz`
- [x] Add error handling to all endpoints → `bd: umbane-7zz`
- [x] Add authentication → `bd: umbane-7zz`

## Priority 3: Frontend ✅ COMPLETE
- [x] Install frontend dependencies (axios, ethers.js) → `bd: umbane-2mn`
- [x] Create wallet connection component → `bd: umbane-bz7`
- [x] Create token mint/burn UI → `bd: umbane-bz7`
- [x] Create balance display component → `bd: umbane-bz7`

## Priority 4: Integration & Testing
- [ ] Configure and deploy to Polygon testnet → `bd: umbane-0o6`

## Future: JSE Integration
- [ ] Research JSE Carbon Credit Trading API → IN PROGRESS
- [ ] Implement gateway for carbon credit trading

## JSE Carbon Trading Research

### JSE Ventures Carbon Market
- **Launch:** February 2025
- **Partner:** Xpansiv (infrastructure provider)
- **First Trade:** 10,000 credits at $8.25/credit
- **Carbon Tax Rate:** R190/ton (~$20.25) - credits cover ~80%

### Integration Options

#### 1. Xpansiv API (Direct)
- **Developer Portal:** https://developer.xpansiv.com/
- **Xpansiv Connect** - Portfolio management REST APIs
- **Marketplace** - FIX API for trading
- **TIGR Registry** - Carbon credit registry
- **NAR Registry** - North American Renewables
- **Capabilities:**
  - Credit inventory across registries
  - Transaction history
  - Initiate bilateral trades
  - Retirements

#### 2. Xpansiv Python SDK
- Runs within Xpansiv application pipelines
- Usage modes:
  - Python Runner task in pipeline
  - Jupyter Notebook in pipeline
  - Container with ensemble of scripts
- **Use cases:** Automated trading, portfolio rebalancing, reporting

#### 3. OpenAPI Endpoints (Xpansiv Connect v1-beta)
```
Accounts          - Account management
Exchange          - Trading operations
Forward Deals     - Forward contracts
Generators        - Energy generators
Instruments       - Available instruments
Issuances         - Credit issuances
Portfolio         - Position management
Projects          - Carbon projects
ReferenceData    - Market data
Reports          - Reporting
Retirements       - Credit retirements
Transfers         - Transfer operations
```

### Implementation Plan
1. Apply for Xpansiv/JSE developer access
2. Integrate Xpansiv Connect API for portfolio view
3. Match on-chain aC tokens with JSE carbon credits
4. Implement retirement/burning mechanism for tax compliance

## Chainlink Integration ✅ COMPLETE (umbane-dut)
- [x] Add Data Feeds integration (AggregatorV3Interface)
- [x] Add carbon price feed configuration
- [x] Add calculateCarbonCredits() for energy-to-carbon conversion
- [x] Add backend endpoints for Chainlink operations
### Current State
- Contract has VRFConsumerBaseV2 (line 8) but placeholder implementation
- `requestEnergyData()` simulates random energy usage (0-999 kWh)

### Recommended Implementation
1. **Data Feeds** - Add carbon credit pricing (USD per ton CO2)
   - Use Chainlink Price Feeds for carbon credit valuation
   - Enable aC token to track market value

2. **Chainlink Automation** - Automate carbon credit calculations
   - Trigger mintAC based on verified energy usage
   - Periodic carbon credit value updates

3. **Custom Data Feed (IoT)** - Connect smart meter data
   - Request custom data feed from Chainlink node operators
   - Or use Chainlink Functions for API aggregation

### Resources
- [Chainlink Data Feeds](https://docs.chain.link/data-feeds)
- [Chainlink Automation](https://docs.chainlink/automation)
- [Carbon Credit Integration](https://chain.link/article/carbon-credit-crypto)
