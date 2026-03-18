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
- [ ] Research JSE Carbon Credit Trading API
- [ ] Implement gateway for carbon credit trading

## Chainlink Research (umbane-dut)
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
