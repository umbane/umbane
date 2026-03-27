# PRD vs Implementation Gap Analysis

## Current Implementation Status

### Smart Contract (Token.sol)

**Implemented:**
- [x] Basic ERC20 token (UMBANE)
- [x] mJ and aC token minting
- [x] Burn functions for both
- [x] Carbon price setting
- [x] Energy recording (oracle callable)
- [x] User energy history
- [x] Pending carbon credits

**Missing:**
- [ ] Grid electricity purchase functions (FR-GP)
- [ ] Token pledge/CarB functionality
- [ ] Electricity tariff storage

### Backend API

**Implemented:**
- [x] Health check
- [x] Auth/login
- [x] Mint/Burn mJ and aC
- [x] Balance queries
- [x] Total supply
- [x] Transaction history
- [x] Carbon price feed integration
- [x] Carbon credits calculation
- [x] Energy processing

**Missing:**
- [ ] ESP device data submission endpoint
- [ ] ESP Oracle verification logic
- [ ] Grid electricity purchase endpoint
- [ ] Token pledge endpoint

### Frontend

**Implemented:**
- [x] Wallet connection (MetaMask)
- [x] Polygon Amoy network detection
- [x] Token balance display
- [x] Carbon calculator
- [x] Token info display
- [x] Mint UI (owner)
- [x] Burn UI

**Missing:**
- [ ] Token trading desk
- [ ] Token retirement
- [ ] Token pledging
- [ ] Grid electricity purchase
- [ ] DAO governance

### Hardware/ESP32

- [ ] Not implemented yet (mentioned in PRD)

---

## Feature Status Summary

| Feature | Status |
|---------|--------|
| ERC20 UMBANE token | Implemented |
| mJ minting | Implemented |
| aC minting | Implemented |
| Burn functions | Implemented |
| Carbon price | Implemented |
| Energy recording | Implemented |
| User history | Implemented |
| Pending credits | Implemented |

---

## Backend API Status

| Endpoint | Status |
|----------|--------|
| /auth/login | Implemented |
| /mintMJ, /mintAc | Implemented |
| /burnMJ, /burnAc | Implemented |
| /balance/* | Implemented |
| /total-supply | Implemented |
| Carbon price feeds | Implemented |
| Carbon calculator | Implemented |

---

## PRD Requirements Gap

| PRD Requirement | Status |
|-----------------|--------|
| FR-DA: CT clamp/ESP32 hardware | Not started |
| FR-OR: ESP Oracle verification | Not implemented |
| FR-TT: Token trading (DEX) | Not started |
| FR-TR: Token retirement | Not started |
| FR-PF: Token pledging/CarB | Not started |
| FR-GP: Grid electricity purchase | Not started |
| DAO governance | Not started |
| City of Cape Town meter API | Not started |

---

## Gap Summary

- **Completed:** ~25%
- **Remaining:** ~75%

---

## Priority Implementation Order

1. ESP Oracle (backend) + device registration
2. Token trading desk (DEX integration)
3. Token retirement with certificates
4. Token pledging/community pool
5. Grid electricity purchase

---

*Contract Address (Amoy):* `0xF5D3E95244E07444eCFFESBF04418cF1Fe398aDe`