# Carbon Market Integration Research

## Date: 2026-03-18

## Summary

Research into carbon market APIs and supplier registration requirements for the Umbane/MECC Carbon Project.

## Carbonmark API Analysis

### What Carbonmark Offers
- REST API for purchasing and retiring carbon credits programmatically
- Free test API keys available (sandbox environment)
- Fractional retirement down to 0.001 tCO₂
- Instant settlement with retirement certificates
- Monthly invoicing (no need to hold inventory)

### API Flow
1. `GET /carbonProjects` - List available projects
2. `GET /products` - List index products (e.g., mco2, bct)
3. `GET /prices` - Get pricing for projects/products
4. `POST /quotes` - Create retirement quote
5. `POST /orders` - Execute retirement
6. `GET /orders` - Check status

### Why Carbonmark Is Not Suitable

**Carbonmark is a marketplace for buying/selling EXISTING carbon credits**, not for:
- Generating new carbon credits
- Onboarding new carbon credit suppliers
- Issuing carbon credits from renewable energy production

The platform requires verified carbon credits already in their system to trade.

## Supplier Registration (JSE Carbon / BigIn)

The supplier listing form asks for carbon standards:
- Verra
- Gold Standard
- Cercarbono
- ICR
- ACR
- CAR
- Puro.Earth
- Open Forest Protocol
- Regen
- CDM
- Other

### Requirements to become a supplier:
1. **Verification** - Must be verified by one or more carbon standards
2. **Technical onboarding** - Means of registering carbon credits from users

## MECC Carbon Project Scope (Actual Requirements)

### What This Project Does
The project enables home solar/prosumer energy producers to earn carbon credits:

1. **Data Acquisition**
   - ESP32 + camera for prepaid meter data
   - Direct solar array metering (open-meter PCB)
   - Chainlink oracle for verification

2. **Token System**
   - `mJ` token - minted per watt of domestic energy produced
   - `aC` token - carbon credit as NFT (ERC-721)
   - `CarB` tokens - from pledging mJ/aC

3. **DAO Governance**
   - NFT holders have voting rights
   - Community decisions on credit issuance

### Current Status (umbane repo)
| Component | Status |
|-----------|--------|
| UMB Token (ERC20) | ✅ Deployed on Polygon Amoy |
| Backend API | ✅ Complete |
| Frontend UI | ✅ Complete |
| Carbonmark Integration | 🔄 Future pathway (market tracking) |
| Hardware/ESP32 | 🔄 In carbon-project repo |

## Recommendations

### Strategic Value of Carbonmark

Despite not being able to issue credits directly, Carbonmark remains strategically important:

1. **Proof of Market Demand**
   - Demonstrates global appetite for carbon credits
   - Can track pricing, volume, and trends
   - Validates business case for R&D funding

2. **Future Integration Pathway**
   - API is ready when we have verified credits
   - Already documented integration patterns
   - No need to build from scratch later

3. **Bypass Local Infrastructure**
   - JSE Carbon Trading is nascent, no API access yet
   - Cape Town lacks a carbon trading desk
   - Carbonmark provides immediate global access

4. **Funding Rationale**
   - Show investors: "Carbonmark exists, market is ready, we need hardware to generate credits"
   - R&D funding for ESP32/meter data acquisition devices
   - Bridge the gap between PoC and verified carbon issuance

### Approach

1. **PoC Phase** (current)
   - Build token system (UMB on Polygon Amoy ✅)
   - Track Carbonmark prices via API
   - Document theoretical carbon credit flow

2. **Verification Phase** (future)
   - Apply for Gold Standard/Verra registration
   - Build hardware (ESP32 + open-meter)
   - Establish DAO governance

3. **Integration Phase**
   - Connect to Carbonmark for resale
   - Or list on other marketplaces

## Next Steps

1. **Add Carbonmark API integration to backend**
   - Track carbon project prices
   - Monitor market trends
   - Store historical data for analytics

2. **Continue PoC development**
   - Test frontend with backend
   - Set up local PostgreSQL

3. **Document funding pitch**
   - Use Carbonmark existence as market validation
   - Focus on hardware (ESP32) for prosumer onboarding

## References

- Carbonmark API: https://docs.carbonmark.com/
- JSE Carbon Trading: https://us.bigin.online/org894283421/forms/new-supplier-listing
- MECC Carbon Project: https://github.com/umbane/carbon-project
- Umbane Token: https://amoy.polygonscan.com/token/0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe
