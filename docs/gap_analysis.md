# Umbane Project Gap Analysis

**Generated:** March 19, 2026  
** PRD Version:** 1.1

---

## Implementation Status Summary

| Component | Completion |
|-----------|------------|
| Smart Contract (Token.sol) | ~85% |
| Backend API | ~70% |
| Frontend (Basic) | ~60% |
| Hardware/Oracle | 0% |
| Trading Desk | 0% |
| Retirement/Pledging | 0% |
| Grid Purchase | 0% |
| DAO Governance | 0% |

---

## ✅ Completed Features

### Smart Contract (Amoy: `0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe`)

| Feature | FR-ID | Status |
|---------|-------|--------|
| ERC20 UMBANE token | - | ✅ Done |
| mJ token minting | FR-TM-01 | ✅ Done |
| aC token minting | FR-TM-02 | ✅ Done |
| Burn mJ tokens | FR-TR-03 | ✅ Done |
| Carbon price tracking | - | ✅ Done |
| Energy recording | FR-TM-03 | ✅ Done |
| User history | FR-TM-03 | ✅ Done |
| Pending credits | FR-TM-04 | ✅ Done |

### Backend API

| Endpoint | Status |
|----------|--------|
| `/auth/login` | ✅ |
| `/mintMJ`, `/mintAC` | ✅ |
| `/burnMJ`, `/burnAC` | ✅ |
| `/balance/*` | ✅ |
| `/total-supply` | ✅ |
| `/transactions/*` | ✅ |
| Carbon price feeds | ✅ |
| Carbon calculator | ✅ |
| `/chainlink/process-energy` | ✅ |

### Frontend

| Feature | Status |
|---------|--------|
| MetaMask wallet connection | ✅ |
| Polygon Amoy network switch | ✅ |
| Token balance display | ✅ |
| Total supply display | ✅ |
| Mint UI (owner only) | ✅ |
| Burn UI | ✅ |
| Carbon calculator | ✅ |
| Token add to wallet | ✅ |

---

## ❌ Missing Features (by PRD Priority)

### Phase 1: Data Acquisition & Oracle

| ID | Feature | FR | Priority |
|----|---------|-----|----------|
| F01 | CT Clamp Hardware Integration | FR-DA-01 | Must |
| F02 | ESP32 Firmware for Energy Measurement | FR-DA-02 | Must |
| F03 | Device Data Signing (ECDSA) | FR-DA-04 | Must |
| F04 | ESP Oracle Backend Service | FR-OR-01 | Must |
| F05 | Signature Verification | FR-OR-01 | Must |
| F06 | Replay Attack Prevention | FR-OR-02 | Must |
| F07 | Oracle Batch Submission | FR-OR-04 | Should |

### Phase 2: Token Trading

| ID | Feature | FR | Priority |
|----|---------|-----|----------|
| F08 | DEX Integration (QuickSwap) | FR-TT-02 | Must |
| F09 | Token Swap UI | FR-TT-01 | Must |
| F10 | Real-time Price Feeds | FR-TT-03 | Must |
| F11 | Liquidity Pool Interface | FR-TT-02 | Should |

### Phase 3: Retirement & Pledging

| ID | Feature | FR | Priority |
|----|---------|-----|----------|
| F12 | Token Retirement Flow | FR-TR-01 | Must |
| F13 | Carbon Certificate Generation | FR-TR-02 | Must |
| F14 | Token Pledging UI | FR-PF-01 | Must |
| F15 | Community Pool Contract | FR-PF-02 | Must |
| F16 | DAO Governance | FR-PF-03 | Should |

### Phase 4: Grid Purchase

| ID | Feature | FR | Priority |
|----|---------|-----|----------|
| F17 | Electricity Tariff Setting | FR-GP-02 | Must |
| F18 | Grid Purchase UI | FR-GP-01 | Must |
| F19 | City of Cape Town API | FR-GP-03 | Must |
| F20 | Hybrid Payment Support | FR-GP-07 | Should |

---

## Implementation Roadmap

```
Month 1-3 (MVP):     [████░░░░░░░░░░░░░░] F01-F07 (Oracle/Data)
Month 4-6 (Beta):   [████████░░░░░░░░░] F08-F11 (Trading Desk)
Month 7-9 (Launch): [████████████░░░░░] F12-F16 (Retire/Pledge)
Month 10-12 (Ext):  [████████████████░] F17-F20 (Grid Purchase)
```

---

## Technical Debt & Notes

1. **Contract ABI Mismatch**: Backend uses `mint()` but contract has `mintMJ()`/`mintAC()` - needs update
2. **No separate mJ/aC tracking**: Contract returns same balance for both - PRD says separate tokens
3. **Database not initialized**: Schema not provided - need `init_db.sql`
4. **No device registry**: Oracle needs to know valid device addresses
5. **No price feed**: Carbon price is manual - needs Chainlink integration

---

## Quick Wins

| Task | Effort | Impact |
|------|--------|--------|
| Fix mint function name in backend | 1hr | High |
| Create database schema | 2hr | High |
| Add device registration endpoint | 4hr | High |
| Implement trading desk UI | 1wk | High |
