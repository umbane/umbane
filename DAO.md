# Umbane DAO

## Overview

Decentralized governance for the Umbane carbon token system, enabling aC token holders to vote on protocol decisions.

---

## Token Structure

| Token | Symbol | Purpose | Voting Power |
|-------|--------|---------|--------------|
| Energy | mJ | Energy production (Wh) | None |
| Carbon | aC | Carbon credits (kg CO2) | 1 aC = 1 vote |

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
| Standard | 100 aC | 4% | Parameter changes, treasury <R100k |
| Major | 100 aC | 10% | Contract upgrades, oracle changes |
| Emergency | Council only | N/A | System pause, security incident |

---

## Setup Checklist

- [ ] Deploy Gnosis Safe on Polygon (4-of-7)
- [ ] Transfer Token.sol ownership to Safe
- [ ] Create governance documentation
- [ ] Set up Discord/Telegram governance channel
- [ ] Distribute initial aC tokens to early adopters

- [ ] Audit Governor + Timelock contracts
- [ ] Deploy Governor.sol on Polygon
- [ ] Upgrade aC token with ERC20Votes
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
| `contracts/Governor.sol` | DAO voting logic |
| `contracts/ACVotes.sol` | aC voting power extension |
| `contracts/Timelock.sol` | Execution delay |

---

## References

- Design: `docs/umbane_dao_governance_analysis.md`
- Implementation: `contracts/Governor.sol`

---

**Status:** Phase 1 active, Phase 2 contract skeleton created