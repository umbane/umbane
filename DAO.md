# Umbane DAO

## Overview

Decentralized governance for the Umbane carbon token system, with **UMB** as the governance token that wraps mJ (energy) and aC (carbon) with REC certificates.

---

## Token Structure

| Token | Symbol | Type | Purpose | REC Certificate |
|-------|--------|------|---------|------------------|
| **Governance** | **UMB** | ERC-20 | Voting + wrapping | Wraps mJ + aC |
| Energy | mJ | ERC-20/721 | Proof of production | None (pending) |
| Carbon | aC | ERC-20 | Attested carbon credits | zaREC/d-REC |

**Flow:**
```
Energy Production → mJ (energy proof)
                        ↓ (wrap with REC)
                     UMB (governance token)
                        ↓ (attest)
                     aC (carbon credit + REC cert)
```

---

## Phased Governance Model

### Phase 1: Multi-Sig Council (Months 1-6)
- **Type:** Gnosis Safe (off-chain, 4-of-7 signatures)
- **Members:** 
  - 2 Umbane founders
  - 2 community representatives
  - 2 technical experts
  - 1 carbon auditor
- **Powers:**
  - Carbon pricing updates
  - REC integration decisions
  - Oracle configuration
  - Emergency system pauses
  - Contract upgrades
- **Status:** Active (no on-chain contract needed)

### Phase 2: Hybrid Governance (Months 6-18)
- **On-chain:** OpenZeppelin Governor + Timelock
- **Voting Token:** UMB (governance token)
- **Parameters:**
  - Voting delay: 2 days
  - Voting period: 5 days
  - Proposal threshold: 100 UMB
  - Quorum: 4%
  - Max voting power: 500 UMB (5% per address)
- **Council Veto:** Retained for 12 months

### Phase 3: Full DAO (Month 18+)
- Remove council veto
- Lower quorum to 2-3%
- Add delegation mechanisms

---

## Phased Governance Model

### Phase 1: Multi-Sig Council (Months 1-6)
- **Type:** Gnosis Safe (off-chain, 4-of-7 signatures)
- **Members:** 
  - 2 Umbane founders
  - 2 community representatives
  - 2 technical experts
  - 1 carbon auditor
- **Powers:**
  - Carbon pricing updates
  - Oracle configuration
  - Emergency system pauses
  - Contract upgrades
- **Status:** Active (no on-chain contract needed)

### Phase 2: Hybrid Governance (Months 6-18)
- **On-chain:** OpenZeppelin Governor + Timelock
- **Voting Token:** aC (requires ERC20Votes extension)
- **Parameters:**
  - Voting delay: 2 days
  - Voting period: 5 days
  - Proposal threshold: 100 aC
  - Quorum: 4%
  - Max voting power: 500 aC (5% per address)
- **Council Veto:** Retained for 12 months

### Phase 3: Full DAO (Month 18+)
- Remove council veto
- Lower quorum to 2-3%
- Add delegation mechanisms
- Sub-committees: Technical, Carbon Verification, Treasury

---

## Proposal Types

| Type | Threshold | Quorum | Examples |
|------|-----------|--------|----------|
| Standard | 100 UMB | 4% | Parameter changes, treasury <R100k |
| Major | 100 UMB | 10% | Contract upgrades, REC registry changes |
| Emergency | Council only | N/A | System pause, security incident |

---

## REC Certificate Integration

**Key Design:** UMB wraps mJ + aC with zaREC/d-REC certificate metadata

| REC Registry | Integration | Status |
|--------------|-------------|--------|
| zaREC | South African voluntary market | Planning |
| I-REC | International standard | Planning |
| d-REC | Domestic RECs | Planning |

**Flow:**
1. Prosumer produces energy → mJ minted
2. mJ wrapped with REC metadata → UMB token
3. UMB attested (oracle + DAO) → aC carbon credit + REC cert
4. aC can be retired (burned) with certificate

---

## Setup Checklist

- [ ] Deploy Gnosis Safe on Polygon (4-of-7)
- [ ] Create UMB governance token (ERC20Votes)
- [ ] Define mJ → UMB wrapping mechanism
- [ ] Transfer Token.sol ownership to Safe
- [ ] Set up Discord/Telegram governance channel

- [ ] Audit Governor + Timelock contracts
- [ ] Deploy Governor.sol on Polygon
- [ ] Integrate UMB with REC certificate metadata
- [ ] Deploy Timelock.sol
- [ ] Test governance on Amoy

- [ ] Remove multi-sig veto power
- [ ] Lower quorum threshold
- [ ] Implement delegation UI

---

## Contracts

| Contract | Purpose |
|----------|---------|
| `contracts/Token.sol` | Main token (mJ + aC) |
| `contracts/UMB.sol` | Governance token (wraps mJ + aC + REC metadata) |
| `contracts/Governor.sol` | DAO voting logic |
| `contracts/ACVotes.sol` | aC voting power extension |
| `contracts/Timelock.sol` | Execution delay |

---

## References

- Design: `docs/umbane_dao_governance_analysis.md`
- Implementation: `contracts/Governor.sol`, `contracts/ACVotes.sol`

---

**Status:** Phase 1 active, token structure updated to include UMB governance token