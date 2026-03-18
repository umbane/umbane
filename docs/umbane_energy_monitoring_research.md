# Data Acquisition Solution Research for Umbane Carbon Credit System

## Executive Summary

This document provides comprehensive research on **non-invasive energy monitoring devices** suitable for measuring domestic solar feed-in production for the Umbane carbon credit tokenization system. The City of Cape Town measures feed-in production for tariff purposes but does not issue carbon credits - our system aims to fill this gap by tokenizing verified energy production.

**Primary Recommendation**: Hybrid approach using **ESP32 + CT Clamp sensors + LoRaWAN** for low-cost, scalable deployment across Cape Town households.

---

## Problem Statement

### Current Situation
- **City of Cape Town**: Measures feed-in tariff production but only provides monetary credit, not carbon credits
- **Prosumers**: Domestic solar producers feed electricity into grid
- **Gap**: No mechanism to tokenize this verified production as carbon credits (aC tokens)
- **Need**: Low-cost, non-invasive device to independently measure and verify energy production

### Requirements for Umbane System
1. **Non-invasive**: No electrical modifications or safety certifications required
2. **Accurate metering**: Measure actual kWh production with ±2% accuracy
3. **Tamper-resistant**: Prevent gaming the system
4. **Blockchain integration**: Send verified data to smart contracts on Polygon
5. **Cost-effective**: <R2000 ($110 USD) per unit for mass deployment
6. **Cape Town compatible**: Work with local electrical infrastructure (230V, 50Hz)
7. **Long-range communication**: Many installations lack reliable WiFi

---

## Solution Architecture Overview

### Recommended System Components

```
┌─────────────────────────────────────────────────────────────┐
│  HOUSEHOLD INSTALLATION                                      │
│                                                              │
│  ┌──────────────┐         ┌─────────────────┐              │
│  │ Solar Panels │────────▶│ Grid Inverter   │              │
│  └──────────────┘         └────────┬────────┘              │
│                                    │                         │
│                                    │ Feed-in Line           │
│                            ┌───────▼────────┐               │
│                            │  CT Clamp       │               │
│                            │  (Non-invasive) │               │
│                            └───────┬────────┘               │
│                                    │                         │
│                            ┌───────▼────────┐               │
│                            │  ESP32 Device   │               │
│                            │  - Measures kWh │               │
│                            │  - Signs data   │               │
│                            │  - Transmits    │               │
│                            └───────┬────────┘               │
│                                    │                         │
│                                    │ LoRaWAN                │
└────────────────────────────────────┼─────────────────────────┘
                                     │
                                     │
                            ┌────────▼─────────┐
                            │  LoRa Gateway    │
                            │  (Community Hub) │
                            └────────┬─────────┘
                                     │
                                     │ 4G/LTE/WiFi
                            ┌────────▼─────────┐
                            │  Backend Server  │
                            │  - Verifies data │
                            │  - Batches txs   │
                            └────────┬─────────┘
                                     │
                                     │ Chainlink Oracle
                            ┌────────▼─────────┐
                            │ Polygon Network  │
                            │ - Mint mJ tokens │
                            │ - Issue aC NFTs  │
                            └──────────────────┘
```

---

## Technology 1: Current Transformer (CT) Clamp Sensors

### What Are CT Clamps?

Current Transformer (CT) clamps are **non-invasive sensors** that measure electrical current flowing through a wire using electromagnetic induction. They clip around the wire without any electrical connection.

### How They Work

1. **Electromagnetic Induction**: AC current in the wire creates a magnetic field
2. **Secondary Coil**: The CT clamp has a ferrite core with a coil that detects this field
3. **Proportional Output**: Produces a small current/voltage proportional to the main current
4. **Safety**: No direct electrical contact with high voltage

### Types Suitable for Umbane

#### Option A: SCT-013 Series (Budget Option)
- **Model**: SCT-013-000 (100A version) or SCT-013-030 (30A version)
- **Cost**: R150-R300 ($8-$17 USD)
- **Output**: 0-1V or 0-50mA
- **Accuracy**: ±1%
- **Aperture**: 13mm (suitable for most household cables)
- **Power**: Passive (no battery)
- **Availability**: Widely available on Takealot, Robot Electronics, Micro Robotics

**Pros**:
- Very cheap
- Easy to source in South Africa
- Proven in DIY energy monitoring
- 3.5mm jack connector (plug-and-play)

**Cons**:
- Lower build quality
- Manual calibration required
- Not weatherproof

#### Option B: Wireless Self-Powered CT Sensors (Premium Option)

**Milesight CT3xx Series**
- **Model**: CT301 (EU868 LoRaWAN)
- **Cost**: R2,500-R3,500 ($140-$195 USD)
- **Output**: Digital LoRaWAN packets
- **Accuracy**: ±1%
- **Power**: Self-powered from measured conductor (no batteries!)
- **Sampling**: 3.3kHz (very high accuracy)
- **Range**: 2-10km LoRaWAN

**Pressac Wireless CT Sensors**
- **Cost**: R2,800-R4,000 ($155-$220 USD)
- **Power**: Energy harvesting from conductor
- **Range**: 1-600A measurement range
- **Communication**: LoRaWAN, cellular, WiFi options

**Pros**:
- No batteries needed (powered by the current itself!)
- Built-in LoRaWAN transmitter
- Industrial-grade accuracy
- Weatherproof enclosures
- CE certified

**Cons**:
- Expensive for mass deployment
- Requires minimum 1A current to power up
- Import costs to South Africa

#### Option C: MultiTech CT300 (Commercial Grade)
- **Cost**: ~R4,500 ($250 USD)
- **Features**: LoRaWAN built-in, cloud platform integration
- **Power**: Self-powered
- **Target**: Commercial/industrial installations

### Installation Considerations

**Correct CT Clamp Installation**:
1. Clamp around **ONE wire only** (Live OR Neutral, not both)
2. Arrow on clamp points toward load (away from source)
3. Installed on the **feed-in line** between inverter and meter
4. Must not clamp around entire cable sheath (would cancel out)

**Safety**:
- Turn off breaker before clamping
- Use voltage tester to confirm wire is de-energized
- Only clamp when circuit is OFF

---

## Technology 2: ESP32 Microcontroller Platform

### Why ESP32?

The ESP32 is a **low-cost, powerful microcontroller** with built-in WiFi, Bluetooth, and extensive community support.

### Key Specifications
- **CPU**: Dual-core 240MHz Xtensa LX6
- **Memory**: 520KB SRAM, 4MB Flash
- **Connectivity**: WiFi (2.4GHz), Bluetooth/BLE
- **GPIO**: Multiple ADC pins for sensor input
- **Power**: 3.3V, can run on battery or USB
- **Cost**: R80-R250 ($4-$14 USD)

### ESP32 Variants for Umbane

#### Standard ESP32 DevKit V1
- **Cost**: R80-R120 ($4-$7 USD)
- **Use case**: WiFi-based installations with power supply
- **Availability**: Robotics.org.za, DIY Electronics, Micro Robotics

#### ESP32 + LoRa Boards (Recommended)

**TTGO T-Beam ESP32 LoRa 868MHz**
- **Cost**: R650-R850 ($36-$47 USD)
- **Features**: 
  - ESP32 + LoRa SX1276 radio (868MHz EU band)
  - GPS module (can add location verification!)
  - Battery management (18650 LiPo)
  - OLED display
- **Range**: 2-15km in urban areas
- **Availability**: Robotics.org.za

**Heltec WiFi LoRa 32 V3**
- **Cost**: R550-R750 ($30-$41 USD)
- **Features**:
  - ESP32-S3 + LoRa SX1262
  - OLED display
  - Lower power consumption than TTGO
- **Availability**: Robotics.org.za, NetRAM

**LilyGO T3-S3 (2026 model)**
- **Cost**: R600-R800
- **Features**: 
  - ESP32-S3 + LoRa SX1262
  - Enhanced security features
  - Better range than older models

### Energy Metering Chip Options

#### PZEM-004T Module (Recommended)
- **Cost**: R250-R400 ($14-$22 USD)
- **Measures**: Voltage, Current, Power, Energy, Frequency, Power Factor
- **Interface**: UART (easy ESP32 integration)
- **Accuracy**: ±0.5% (better than basic CT clamps alone)
- **Safety**: Optical isolation from mains
- **Availability**: Amazon, AliExpress, DIY Electronics SA

**Why PZEM + CT Clamp?**
The PZEM module can work with external CT clamps OR measure directly. For non-invasive setup, use external CT clamp with PZEM for processing.

#### ATM90E32AS Chip (Advanced)
- **Cost**: R800-R1,200 (module + components)
- **Accuracy**: ±0.1%
- **Features**: 3-phase metering, anti-tamper
- **Use case**: High-value installations, commercial prosumers

---

## Technology 3: LoRaWAN Connectivity

### Why LoRaWAN for Umbane?

1. **Long Range**: 2-15km in urban Cape Town, up to 50km rural
2. **Low Power**: Battery life of 5-10 years on coin cell
3. **No WiFi Required**: Most households don't have reliable WiFi near inverter
4. **Penetrates Buildings**: Better than WiFi through walls
5. **Low Cost**: No cellular data fees
6. **Secure**: AES-128 encryption built-in

### LoRaWAN Architecture for Cape Town

#### Community Gateway Model (Recommended)

**Deployment Strategy**:
- Deploy **1 LoRa gateway per neighborhood** (covers 100-500 homes)
- Gateways connect to internet via 4G/LTE or fixed WiFi
- Individual homes only need low-cost LoRa sensor nodes
- Gateways are funded by Umbane or local energy cooperatives

**Gateway Options**:

**SenseCAP M2 Multi-Platform Gateway (SX1302)**
- **Cost**: R4,500-R6,500 ($250-$360 USD)
- **Features**:
  - SX1302 chipset (latest gen)
  - 8 channels
  - 10km+ urban range
  - Ethernet + WiFi + 4G options
  - The Things Network (TTN) compatible
- **Coverage**: 200-500 devices
- **Availability**: Robotics.org.za, import from Seeed Studio

**RAKwireless WisGate Edge Lite 2**
- **Cost**: R5,500-R7,500 ($305-$415 USD)
- **Features**: Industrial gateway, outdoor rated, solar compatible
- **Coverage**: 500+ devices

**Community Gateway Locations in Cape Town**:
- Solar PV installation companies (Solid Solar, Solar Advice)
- Municipal buildings with feed-in agreements
- Community centers in Southern Suburbs, Atlantic Seaboard
- Energy cooperatives (Muizenberg Electricity Cooperative)

#### Network Server Options

**The Things Network (TTN)** - FREE
- Free LoRaWAN network server
- Active South Africa community
- Cape Town already has some gateways
- 30-second uplink limit (fair use)
- **Best for**: Pilot phase (first 100-500 homes)

**Chirpstack** - SELF-HOSTED
- Open-source LoRaWAN server
- Run on your own infrastructure
- No device limits
- **Best for**: Production scale (1000+ homes)

**Helium Network** - CRYPTO-INCENTIVIZED
- Decentralized LoRa network
- Gateway operators earn HNT tokens
- Growing in South Africa
- **Best for**: Aligning with Umbane's crypto ethos

---

## Complete Device Design Options

### Option 1: Budget DIY Kit (R800-R1,200 / $44-$66)

**Components**:
- ESP32 DevKit: R100
- SCT-013-030 CT Clamp: R200
- PZEM-004T module: R350
- Enclosure (weatherproof ABS box): R80
- 5V power supply: R70
- Prototype board, wires, connectors: R100
- LoRa module (RFM95W 868MHz): R300

**Total**: ~R1,200 ($66 USD)

**Communication**: Requires LoRa gateway OR WiFi

**Pros**:
- Lowest cost
- Can be assembled locally (STEAM education opportunity!)
- Easy to repair

**Cons**:
- Manual assembly required
- No certifications
- Reliability varies

**Best for**: Pilot program, early adopters, Muizenberg Electricity Cooperative members

---

### Option 2: Integrated LoRa Monitoring Device (R1,800-R2,500 / $100-$138)

**Components**:
- TTGO T-Beam ESP32 LoRa 868MHz: R750
- SCT-013-100 CT Clamp: R250
- Custom PCB (designed by Umbane, manufactured at NextPCB): R400
- Weatherproof DIN rail enclosure: R200
- 18650 LiPo battery + solar trickle charger: R300
- Assembly & testing: R200

**Total**: ~R2,100 ($116 USD)

**Communication**: LoRaWAN only (requires gateway)

**Pros**:
- Professional design
- Battery-powered (works during load shedding!)
- GPS location verification
- 2-15km range without WiFi
- Low maintenance (5+ year battery life with solar)

**Cons**:
- Requires community LoRa gateway
- Higher upfront cost

**Best for**: Scale deployment (100+ homes), suburban Cape Town

---

### Option 3: Premium Self-Powered Wireless CT (R3,000-R4,000 / $166-$220)

**Components**:
- Milesight CT301 LoRaWAN sensor: R3,200
- Configuration & installation: R500

**Total**: ~R3,700 ($205 USD)

**Communication**: LoRaWAN built-in

**Pros**:
- Zero maintenance (no batteries!)
- Industrial accuracy (±1%)
- CE certified (regulatory compliance)
- Plug-and-play
- 10+ year lifespan

**Cons**:
- High cost per unit
- Requires minimum 1A current (won't work on very low production)
- Import lead times

**Best for**: High-value commercial installations, affluent neighborhoods, pilot with solar companies

---

## Blockchain Integration Architecture

### Data Flow: Sensor to Smart Contract

```
Step 1: MEASUREMENT
├─ CT Clamp measures current on feed-in line
├─ ESP32 calculates: I (amps), V (volts), P (watts), E (kWh)
└─ Sampling rate: 1 measurement/second, aggregated every 15 minutes

Step 2: LOCAL SIGNING
├─ ESP32 has unique private key (stored in secure flash)
├─ Creates data packet: {device_id, timestamp, energy_kwh, signature}
├─ Signs packet with ECDSA (secp256k1, same as Ethereum)
└─ Tamper-proof: Any modification breaks signature

Step 3: TRANSMISSION
├─ LoRaWAN: Sends to nearest gateway (range 2-15km)
├─ Gateway forwards to backend via internet
└─ Fallback: WiFi direct to backend if available

Step 4: BACKEND VERIFICATION
├─ Verifies signature matches registered device
├─ Checks for duplicate submissions (prevent replay attacks)
├─ Validates timestamp (reject old data)
├─ Aggregates data: 96 readings/day → daily total
└─ Batches multiple users' data for gas efficiency

Step 5: ORACLE SUBMISSION
├─ Backend acts as Chainlink node (trusted oracle)
├─ OR use Chainlink External Adapter
├─ Batches 10-50 users' data per transaction
├─ Posts to Polygon smart contract: recordEnergyUsage()
└─ Gas cost: ~0.001 MATIC per transaction

Step 6: TOKEN MINTING
├─ Smart contract verifies oracle signature
├─ Mints mJ tokens (energy produced)
├─ Queues aC tokens (carbon credits) for verification
└─ Emits event: EnergyRecorded(user, kwh, timestamp)
```

### Security Measures

#### Device-Level Security
1. **Unique Device ID**: Each ESP32 has hardware-based unique ID
2. **Private Key Storage**: Stored in ESP32 flash (encrypted with device ID)
3. **Secure Boot**: Enable ESP32 secure boot to prevent firmware tampering
4. **OTA Updates**: Signed firmware updates via LoRaWAN

#### Backend Security
1. **Signature Verification**: Reject any unsigned or improperly signed data
2. **Rate Limiting**: Max 96 readings/day per device (1 every 15 min)
3. **Anomaly Detection**: Flag unusual production spikes (>10kW for residential)
4. **Geofencing**: GPS data (if available) confirms device in Cape Town

#### Smart Contract Security
1. **Oracle Whitelist**: Only authorized Chainlink nodes can submit
2. **Pause Mechanism**: Admin can pause in case of attack
3. **Rate Limits**: Max mJ minting per address per day
4. **Time-locks**: 24-hour delay on large aC claims

---

## Cost Analysis & Economics

### Per-Device Costs (Scale: 1,000 Units)

| Component | Budget Option | Mid-Range Option | Premium Option |
|-----------|---------------|------------------|----------------|
| Microcontroller | R100 (ESP32) | R750 (TTGO T-Beam) | R3,200 (Milesight CT) |
| CT Sensor | R200 (SCT-013) | R250 (SCT-013-100) | Included |
| Energy IC | R350 (PZEM) | Included in PCB | Included |
| LoRa Module | R300 (RFM95) | Included | Included |
| Enclosure | R80 | R200 (DIN rail) | Included |
| Power Supply | R70 | R300 (battery+solar) | Self-powered |
| PCB & Assembly | R100 | R400 | R500 (config) |
| **TOTAL** | **R1,200 ($66)** | **R2,100 ($116)** | **R3,700 ($205)** |

### Gateway Costs (Per Community Hub)

| Component | Cost (ZAR) | Cost (USD) |
|-----------|-----------|-----------|
| SenseCAP M2 Gateway | R5,500 | $305 |
| 4G LTE Modem (if no WiFi) | R800 | $44 |
| Outdoor Enclosure | R600 | $33 |
| Installation & Mounting | R1,000 | $55 |
| **TOTAL PER GATEWAY** | **R7,900** | **$437** |
| **Covers** | 200-500 homes | |
| **Cost per home** | R16-40 | $0.87-$2.19 |

### Backend Infrastructure Costs

| Component | Monthly Cost (ZAR) | Monthly Cost (USD) |
|-----------|-------------------|-------------------|
| Server (DigitalOcean 4GB VPS) | R650 | $36 |
| Chirpstack LoRa Network Server | Free (self-hosted) | Free |
| Database (PostgreSQL + TimescaleDB) | R400 | $22 |
| Chainlink Node Operation | R800 | $44 |
| Domain & SSL Certs | R100 | $5.50 |
| Monitoring (Grafana Cloud) | R200 | $11 |
| **TOTAL MONTHLY** | **R2,150** | **$119** |
| **Cost per home (1000 users)** | R2.15/month | $0.12/month |

### Total Deployment Cost for 1,000 Homes

**Scenario: Mid-Range Option**

| Item | Calculation | Cost (ZAR) | Cost (USD) |
|------|-------------|-----------|-----------|
| 1,000 sensor devices | 1,000 × R2,100 | R2,100,000 | $116,000 |
| 5 community gateways | 5 × R7,900 | R39,500 | $2,185 |
| Backend setup (one-time) | Server config | R20,000 | $1,100 |
| **TOTAL CAPEX** | | **R2,159,500** | **$119,285** |
| Backend operations | R2,150/month × 12 | R25,800/year | $1,428/year |
| **COST PER HOME** | | **R2,185** | **$121** |

### Revenue Model for Cost Recovery

**Assumptions**:
- Average Cape Town household with solar: 10 kWh/day production
- Carbon credit rate: R150/ton CO2 (JSE Carbon Credit spot price 2026)
- Emission factor: 0.9 kg CO2/kWh (Eskom grid average)

**Carbon Credits per Home per Year**:
- Production: 10 kWh/day × 365 days = 3,650 kWh/year
- CO2 offset: 3,650 kWh × 0.9 kg/kWh = 3,285 kg = 3.285 tons CO2
- Value: 3.285 tons × R150/ton = **R493/year**

**Umbane Platform Fee Options**:
1. **10% platform fee**: R49/year per home (payback in 44 years - not viable)
2. **Device rental model**: R50/month for device + monitoring = R600/year (profitable)
3. **Upfront sale + 5% ongoing**: Sell device for R2,100 + R25/year = sustainable

**Recommended Model**: Upfront device sale + small ongoing fee (5-10%) for backend/oracle costs

---

## Implementation Roadmap

### Phase 1: Proof of Concept (Months 1-3)

**Goal**: Deploy 10 devices in Muizenberg area

**Actions**:
1. **Week 1-2**: Source components
   - Order 10× SCT-013-030 CT clamps
   - Order 10× ESP32 DevKit boards
   - Order 10× PZEM-004T modules
   - Order 1× RFM95 LoRa modules or TTGO T-Beams

2. **Week 3-4**: Firmware development
   - ESP32 code for energy measurement
   - Data packet signing (ECDSA)
   - LoRaWAN integration (if using)
   - WiFi fallback

3. **Week 5-6**: Backend development
   - API endpoint for data ingestion
   - Signature verification
   - Database storage (PostgreSQL)
   - Chainlink oracle integration

4. **Week 7-8**: Smart contract updates
   - Modify Token.sol to accept oracle data
   - Deploy to Polygon Mumbai testnet
   - Test recordEnergyUsage() function

5. **Week 9-10**: Pilot deployment
   - Install 10 devices at friendly homes
   - Configure LoRa gateway OR WiFi
   - Monitor data flow

6. **Week 11-12**: Iteration
   - Fix bugs
   - Optimize battery life
   - Calibrate sensors
   - Document installation process

**Budget**: R50,000 ($2,760)

---

### Phase 2: Community Pilot (Months 4-9)

**Goal**: 100 homes in Southern Suburbs + Atlantic Seaboard

**Actions**:
1. **Months 4-5**: Manufacturing
   - Design custom PCB (EasyEDA or KiCad)
   - Order 100 PCBs from NextPCB
   - Bulk order components (Mouser, Arrow)
   - Assemble in-house or contract manufacturer

2. **Month 6**: Gateway deployment
   - Install 3× LoRa gateways:
     - Muizenberg (community center)
     - Fish Hoek (library)
     - Kalk Bay (solar installer partner)
   - Configure Chirpstack server

3. **Months 7-8**: User onboarding
   - Partner with local solar installers
   - Train installers on device setup
   - Create installation guide (with photos)
   - Deploy devices

4. **Month 9**: Monitoring & optimization
   - Track uptime (target: >98%)
   - Measure battery life
   - Analyze data quality
   - Gather user feedback

**Budget**: R350,000 ($19,340)

---

### Phase 3: Scale Deployment (Months 10-24)

**Goal**: 1,000+ homes across Cape Town

**Actions**:
1. **Secure funding**:
   - Apply for grants (South African Green Fund, WWF)
   - Partner with solar companies (subsidized devices)
   - Token sale (aC governance token)

2. **Manufacturing scale-up**:
   - Contract manufacturer in South Africa (reduces import costs)
   - Certify devices (ICASA for radio, SANS for electrical)
   - Establish repair/replacement program

3. **Expand coverage**:
   - 15+ gateways across Cape Town metro
   - Partner with municipalities (Stellenbosch, Paarl)
   - Integrate with existing solar monitoring systems

4. **Carbon credit marketplace**:
   - JSE Carbon Credit API integration
   - aC token listing on DEX (Uniswap, QuickSwap)
   - Partnership with KlimaDAO or Toucan Protocol

**Budget**: R3,000,000 ($165,750)

---

## Technical Specifications

### Device Firmware (ESP32)

**Key Libraries**:
- `EmonLib` - Energy monitoring
- `LoRa` or `LMIC` - LoRaWAN protocol
- `WiFi` - WiFi connectivity (fallback)
- `ArduinoJson` - JSON serialization
- `mbedtls` - Cryptographic signing
- `SPIFFS` - File system (store keys)

**Sample Data Packet** (JSON):
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

**Data Transmission Schedule**:
- Measure: Every 1 second
- Aggregate: Every 15 minutes (96 readings/day)
- Transmit: Every 15 minutes OR batch hourly (save power)

---

### Backend API

**Endpoints**:

`POST /api/v1/energy/submit`
- Accepts signed energy data from devices
- Verifies signature
- Stores in database
- Returns: `{status: "accepted", tx_hash: "0x..."}`

`GET /api/v1/energy/{device_id}/daily`
- Returns daily energy production for device
- Used for user dashboard

`POST /api/v1/oracle/batch-submit`
- Internal endpoint for Chainlink node
- Batches multiple users' data
- Calls smart contract `recordEnergyUsage()`

**Database Schema** (PostgreSQL):
```sql
CREATE TABLE energy_readings (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(64) NOT NULL,
    user_address VARCHAR(42) NOT NULL,
    timestamp BIGINT NOT NULL,
    voltage DECIMAL(5,2),
    current DECIMAL(6,3),
    power DECIMAL(8,2),
    energy_kwh DECIMAL(10,4) NOT NULL,
    signature TEXT NOT NULL,
    verified BOOLEAN DEFAULT false,
    blockchain_tx VARCHAR(66),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_device_timestamp ON energy_readings(device_id, timestamp);
CREATE INDEX idx_user_timestamp ON energy_readings(user_address, timestamp);
```

---

## Regulatory & Compliance Considerations

### South African Regulations

#### ICASA (Independent Communications Authority of SA)
**Radio Frequency Spectrum**:
- LoRa 868MHz falls under **short-range devices**
- **Exempt from licensing** if:
  - Power <10mW ERP
  - Duty cycle <10%
  - LoRaWAN standard complies
- **Action**: Confirm with ICASA Type Approval for LoRa devices

#### SANS (South African National Standards)
**Electrical Safety**:
- **SANS 164-1**: Wiring of premises
- **SANS 1474**: Energy metering equipment
- **Action**: CT clamps are non-invasive (lower risk), but device should not modify electrical installation
- **Insurance**: Liability insurance for device malfunction

#### National Treasury - Carbon Tax Act
**Carbon Credits**:
- Umbane aC tokens must map to **verified emission reductions**
- Consider: Gold Standard, VCS (Verified Carbon Standard), or local certification
- **Action**: Engage with Carbon Tax unit for recognition

#### Financial Sector Conduct Authority (FSCA)
**Crypto Assets**:
- aC tokens as carbon credits may be regulated
- If aC has monetary value, may be considered "crypto asset"
- **Action**: Legal opinion on token classification

### City of Cape Town Requirements

**Feed-in Tariff Program**:
- Prosumers already registered with City
- Umbane devices measure same production
- **Opportunity**: City could recognize aC tokens for rebates/incentives

**Smart Meter Rollout**:
- Cape Town rolling out smart meters (P1 port)
- Future: Direct data from smart meters (no CT clamp needed)
- **Action**: Plan integration pathway

---

## Competitive Analysis

### Existing Energy Monitoring Solutions

#### Shelly EM
- **Cost**: R1,800 ($100 USD)
- **Features**: WiFi, 2-channel CT monitoring, cloud dashboard
- **Pros**: Proven product, easy setup
- **Cons**: Requires WiFi, closed ecosystem, no blockchain integration
- **Verdict**: Good for home monitoring, but can't integrate with Umbane smart contracts

#### Sense Energy Monitor
- **Cost**: R5,500 ($305 USD)
- **Features**: AI-powered device detection, cloud analytics
- **Cons**: Expensive, requires installation by electrician, no open API
- **Verdict**: Not suitable for Umbane (closed system)

#### IoTaWatt
- **Cost**: R3,200 ($177 USD)
- **Features**: Open-source, 14 CT inputs, local data storage
- **Pros**: Very accurate, open platform
- **Cons**: No built-in blockchain, requires manual API integration
- **Verdict**: Could be integrated, but expensive for mass deployment

#### Solar Inverter Monitoring (Enphase, SolarEdge)
- **Cost**: Built into inverter
- **Features**: Cloud dashboards, production monitoring
- **Cons**: Closed APIs, vendor lock-in, no carbon credit tokenization
- **Verdict**: Complementary data source, but not sufficient alone

### Umbane's Competitive Advantages

1. **Carbon Credit Focus**: Only solution that tokenizes production as aC NFTs
2. **Blockchain Native**: Direct integration with Polygon smart contracts
3. **LoRaWAN Option**: Works without WiFi (many inverters in garages/outbuildings)
4. **Open Source**: Community can audit, verify, improve
5. **Local Focus**: Designed for Cape Town's specific needs (load shedding, feed-in tariffs)

---

## Risks & Mitigation Strategies

### Technical Risks

**Risk 1: Data Accuracy**
- **Impact**: Incorrect kWh measurements → wrong token minting
- **Mitigation**: 
  - Use calibrated PZEM modules (±0.5% accuracy)
  - Cross-reference with City meter data (where available)
  - Anomaly detection (flag >10kW residential)
  - Periodic re-calibration program

**Risk 2: Device Tampering**
- **Impact**: Users manipulate devices to fake production
- **Mitigation**:
  - Tamper-evident seals on enclosures
  - GPS verification (T-Beam has built-in GPS)
  - Cross-reference with solar inverter data APIs
  - Community reporting mechanism (fraud bounties)

**Risk 3: LoRa Coverage Gaps**
- **Impact**: Devices can't transmit in some areas
- **Mitigation**:
  - WiFi fallback mode
  - Store-and-forward (buffer data locally)
  - Deploy additional gateways in gaps
  - Partner with Helium Network for coverage

**Risk 4: Backend Downtime**
- **Impact**: Data loss, delayed token minting
- **Mitigation**:
  - Redundant servers (AWS + DigitalOcean)
  - Local data buffering on devices (7 days)
  - Automated failover
  - 99.9% uptime SLA

### Regulatory Risks

**Risk 5: ICASA Enforcement**
- **Impact**: LoRa devices deemed illegal
- **Mitigation**:
  - Obtain Type Approval early
  - Limit power to <10mW
  - Use certified LoRa modules (Semtech SX1276 is approved)

**Risk 6: Carbon Credit Non-Recognition**
- **Impact**: aC tokens not accepted by JSE/CTSE
- **Mitigation**:
  - Engage regulators early (National Treasury)
  - Partner with certified verifier (Gold Standard SA)
  - Focus on voluntary carbon market first

### Economic Risks

**Risk 7: Low Adoption**
- **Impact**: Can't achieve scale economics
- **Mitigation**:
  - Partner with solar installers (include device with new installations)
  - Subsidize initial rollout (grants, token sale)
  - Gamification (leaderboards for top producers)

**Risk 8: Token Price Volatility**
- **Impact**: aC token value crashes, users lose interest
- **Mitigation**:
  - Peg aC to stable carbon credit index
  - Treasury reserves to stabilize
  - Focus on utility (governance) not speculation

---

## Recommended Next Steps (This Month)

### Week 1: Component Sourcing
- [ ] Order 5× SCT-013-030 CT clamps from Robot Electronics (R1,000)
- [ ] Order 5× ESP32 DevKit V1 from Robotics.org.za (R500)
- [ ] Order 5× PZEM-004T modules from DIY Electronics (R1,750)
- [ ] Order 1× TTGO T-Beam for testing (R750)

### Week 2: Development Environment
- [ ] Set up Arduino IDE with ESP32 board support
- [ ] Install required libraries (EmonLib, LoRa, ArduinoJson)
- [ ] Clone Umbane repo, review existing smart contracts
- [ ] Set up test Polygon wallet with Mumbai testnet MATIC

### Week 3: Prototype Build
- [ ] Wire up first prototype (ESP32 + CT clamp + PZEM)
- [ ] Write firmware for energy measurement
- [ ] Test on actual solar inverter feed-in line
- [ ] Validate kWh readings against inverter display

### Week 4: Blockchain Integration
- [ ] Write data signing function (ECDSA)
- [ ] Set up local backend API (Flask/FastAPI)
- [ ] Test end-to-end: sensor → backend → smart contract
- [ ] Deploy to Mumbai testnet, mint test mJ tokens

### Week 5: Documentation & Planning
- [ ] Document prototype results
- [ ] Create installation guide with photos
- [ ] Calculate accurate costs for 100-unit run
- [ ] Identify 10 pilot users in Muizenberg

---

## Conclusion & Recommendations

### Primary Recommendation: Hybrid Approach

**For Pilot (First 100 Homes)**:
- **Device**: ESP32 + SCT-013 CT Clamp + PZEM-004T
- **Cost**: R1,200/device
- **Communication**: WiFi (simple, works with existing infrastructure)
- **Why**: Lowest cost, fastest deployment, learn user needs

**For Scale (1,000+ Homes)**:
- **Device**: TTGO T-Beam (ESP32 + LoRa + GPS) + SCT-013 + Custom PCB
- **Cost**: R2,100/device
- **Communication**: LoRaWAN (5 gateways cover Cape Town metro)
- **Why**: No WiFi needed, tamper-resistant (GPS), sustainable model

### Alternative: Premium Partnership

Partner with **solar installation companies** to bundle premium devices:
- Device: Milesight CT301 self-powered LoRaWAN sensor (R3,700)
- Installed with new solar systems
- Companies add cost to installation package
- Umbane provides backend + carbon credit marketplace
- Revenue share: 20% to installer, 10% to Umbane

### Key Success Factors

1. **Start Small**: 10-device pilot in friendly community (Muizenberg)
2. **Partner Locally**: Solar installers, electricians, energy co-ops
3. **Open Source**: Build community trust through transparency
4. **Regulatory Engagement**: Work with City, ICASA, National Treasury early
5. **User Education**: Most people don't understand carbon credits - invest in education
6. **Interoperability**: Make it easy to integrate with existing solar monitoring

### This Solves Your Core Problem

✅ **Non-invasive**: CT clamps require no electrical work
✅ **Accurate**: ±1% accuracy suitable for carbon credit verification
✅ **Affordable**: R1,200-R2,100 per home at scale
✅ **Blockchain-ready**: ESP32 can sign data, integrate with Polygon
✅ **Independent**: Not reliant on City of Cape Town's metering
✅ **Scalable**: LoRaWAN covers 100-500 homes per gateway

The technology exists, is proven, and is available in South Africa. The missing piece is integration with your smart contracts - which is exactly what Umbane is building.

---

**Document Prepared For**: Umbane Project  
**Date**: March 18, 2026  
**Version**: 1.0  
**Next Review**: After prototype testing (Month 2)

## Appendices

### Appendix A: Bill of Materials (BOM) - Budget Option

| Component | Quantity | Unit Cost (ZAR) | Supplier | Link |
|-----------|----------|----------------|----------|------|
| ESP32 DevKit V1 | 1 | R100 | Robotics.org.za | robotics.org.za/ESP32-DEV |
| SCT-013-030 CT Clamp | 1 | R200 | Robot Electronics | robotelectronics.co.za |
| PZEM-004T Module | 1 | R350 | DIY Electronics | diyelectronics.co.za |
| RFM95W LoRa Module | 1 | R300 | Robotics.org.za | robotics.org.za/RFM95 |
| Waterproof Enclosure | 1 | R80 | Communica | communica.co.za |
| 5V 2A Power Supply | 1 | R70 | Takealot | takealot.com |
| Dupont Wires | 20 | R30 | Robotics.org.za | robotics.org.za |
| Prototype Board | 1 | R40 | Micro Robotics | microrobotics.co.za |
| **TOTAL** | | **R1,170** | | |

### Appendix B: South African Suppliers

**Electronics Components**:
- Robotics.org.za (Cape Town-based, fast shipping)
- Micro Robotics (Johannesburg)
- DIY Electronics (Online)
- NetRAM (Pretoria)
- Communica (Countrywide)
- Takealot (General electronics)

**PCB Manufacturing**:
- ASIC Design Services (Cape Town) - Local PCB fabrication
- NextPCB (China) - Affordable, 5-day turnaround
- JLCPCB (China) - Cheapest option

**LoRa Gateways**:
- Robotics.org.za (RAKwireless, Heltec)
- Seeed Studio (direct import)
- The Things Shop (EU, import)

### Appendix C: Useful Resources

**Open Source Projects**:
- OpenEnergyMonitor: https://openenergymonitor.org/
- ESPHome Energy Monitoring: https://esphome.io/components/sensor/ct_clamp.html
- LoRaWAN Energy Meter (GitHub): https://github.com/WGLabz/LoRaWAN-Energy-Meter

**LoRaWAN in South Africa**:
- The Things Network Cape Town: https://www.thethingsnetwork.org/community/cape-town/
- South African LoRa Alliance: https://www.lora-alliance.org/

**Carbon Credits**:
- JSE Carbon Credit Spot Price: https://www.jse.co.za/
- Gold Standard South Africa: https://www.goldstandard.org/
- Carbon Tax South Africa: https://www.sars.gov.za/types-of-tax/carbon-tax/

**Umbane Existing Repos**:
- Main repo: github.com/umbane/umbane
- Carbon project: github.com/umbane/carbon-project
