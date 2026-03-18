# Umbane Token System Documentation

## Smart Contract

### Contract: `Token.sol`

**Token Name:** UmbaneToken (UMB)

**Description:** ERC20 token contract with Chainlink integration for energy and carbon credit tracking.

#### Token Types
- **mJ (milliJoules)** - Energy token (1 mJ = 1 Wh)
- **aC (arbitrary Carbon)** - Carbon credit token (1 aC = 1 kg CO2 offset)

#### Key Functions

##### Token Operations
| Function | Description |
|----------|-------------|
| `mintMJ(address to, uint256 amount)` | Mint energy tokens |
| `mintAC(address to, uint256 amount)` | Mint carbon credit tokens |
| `burnMJ(uint256 amount)` | Burn energy tokens |
| `burnAC(uint256 amount)` | Burn carbon credit tokens |
| `getMJBalance(address account)` | Get mJ balance |
| `getACBalance(address account)` | Get aC balance |

##### Chainlink Integration
| Function | Description |
|----------|-------------|
| `setCarbonPriceFeed(address _feedAddress)` | Set Chainlink data feed for carbon pricing |
| `updateCarbonPrice()` | Fetch latest carbon price from oracle |
| `getCarbonPrice()` | Get current carbon price (returns price, timestamp) |
| `calculateCarbonCredits(uint256 energyKWh)` | Calculate carbon credits from energy usage |
| `getCarbonValueUSD(uint256 acAmount)` | Calculate USD value of carbon credits |

##### Energy Records
| Function | Description |
|----------|-------------|
| `requestEnergyData(address user)` | Request random energy data (VRF) |
| `processEnergyRecord(address user)` | Process pending energy and mint carbon credits |
| `getUserPendingCredits(address user)` | Get pending carbon credits |
| `getUserEnergyHistory(address user)` | Get user's energy record history |

#### Carbon Calculation
```
Energy (kWh) → CO2 (kg) → Carbon Credits
1 kWh ≈ 500g CO2
1 aC = 1 kg CO2 offset
```

#### Variables
| Variable | Type | Description |
|----------|------|-------------|
| `mJTotalSupply` | uint256 | Total minted mJ tokens |
| `aCTotalSupply` | uint256 | Total minted aC tokens |
| `latestCarbonPrice` | int256 | Current carbon price from oracle |
| `latestCarbonPriceTimestamp` | uint256 | Last price update timestamp |
| `CARBON_CREDIT_KG_FACTOR` | uint256 | = 1000 (kg conversion) |

---

## Backend API Endpoints

### Authentication

#### POST `/auth/login`
Wallet-based authentication.

**Request:**
```json
{
  "wallet_address": "0x...",
  "signature": "0x..."
}
```

**Response:**
```json
{
  "token": "eyJ...",
  "wallet_address": "0x..."
}
```

### Token Operations

#### POST `/mintMJ`
Mint energy tokens.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "address": "0x...",
  "amount": 1000
}
```

#### POST `/mintAC`
Mint carbon credit tokens.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "address": "0x...",
  "amount": 500
}
```

#### POST `/burnMJ`
Burn energy tokens.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "amount": 100
}
```

#### POST `/burnAC`
Burn carbon credit tokens.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "amount": 50
}
```

### Queries

#### GET `/balance/{token_type}/{address}`
Get token balance.

**Token Types:** `mJ`, `aC`

**Response:**
```json
{
  "address": "0x...",
  "token_type": "mJ",
  "balance": "1000"
}
```

#### GET `/transactions/{address}`
Get transaction history.

**Query Params:** `limit`, `offset`

**Response:**
```json
{
  "transactions": [
    {
      "id": 1,
      "token_type": "mJ",
      "amount": "1000",
      "type": "mint",
      "tx_hash": "0x...",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### Chainlink Operations

#### POST `/chainlink/price-feed/set`
Set carbon price feed address.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "feed_address": "0x..."
}
```

#### POST `/chainlink/price-feed/update`
Update carbon price from oracle.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "tx_hash": "0x...",
  "price": 50000000,
  "timestamp": 1704067200,
  "status": "success"
}
```

#### GET `/chainlink/price-feed/get`
Get current carbon price.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "price": 50000000,
  "timestamp": 1704067200
}
```

#### GET `/chainlink/calculate-credits`
Calculate carbon credits from energy.

**Headers:** `Authorization: Bearer <token>`

**Query:** `?energy_kwh=100`

**Response:**
```json
{
  "energy_kwh": 100,
  "carbon_credits": 50000,
  "calculation": "100 kWh * 500g CO2/kWh = 50000kg CO2"
}
```

#### GET `/chainlink/carbon-value`
Get USD value of carbon credits.

**Headers:** `Authorization: Bearer <token>`

**Query:** `?amount=1000`

**Response:**
```json
{
  "ac_amount": 1000,
  "usd_value": 50,
  "note": "Value in USD (assuming price feed is set)"
}
```

#### POST `/chainlink/process-energy`
Process pending energy records and mint carbon credits.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "user_address": "0x..."
}
```

### Health Check

#### GET `/health`
Check system status.

**Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "web3": "connected"
}
```

---

## Environment Variables

### Backend
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/umbane` |
| `SECRET_KEY` | JWT signing key | `dev-secret-key-change-in-production` |
| `POLYGON_PROVIDER_URL` | Polygon RPC URL | `https://rpc-amoy.polygon.tech` |
| `CONTRACT_ADDRESS` | Deployed contract address | `0x0000...` |
| `ACCOUNT_ADDRESS` | Deployer wallet address | `0x0000...` |
| `ACCOUNT_PRIVATE_KEY` | Private key for transactions | (empty) |

### Frontend
| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:5000` |
