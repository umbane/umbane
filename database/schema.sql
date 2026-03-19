-- Umbane Token System Database Schema

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    wallet_address VARCHAR(42) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Token balances table
CREATE TABLE IF NOT EXISTS token_balances (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token_type VARCHAR(10) NOT NULL, -- 'mJ' or 'aC'
    balance NUMERIC(78, 0) DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, token_type)
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    user_address VARCHAR(42) NOT NULL,
    token_type VARCHAR(10) NOT NULL, -- 'mJ' or 'aC'
    amount NUMERIC(78, 0) NOT NULL,
    type VARCHAR(10) NOT NULL, -- 'mint' or 'burn'
    tx_hash VARCHAR(66) UNIQUE,
    block_number BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy usage records (for oracle data)
CREATE TABLE IF NOT EXISTS energy_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    energy_used_kwh NUMERIC(20, 2),
    source VARCHAR(50), -- 'chainlink', 'manual', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_wallet ON users(wallet_address);
CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_address);
CREATE INDEX IF NOT EXISTS idx_transactions_tx_hash ON transactions(tx_hash);
CREATE INDEX IF NOT EXISTS idx_energy_records_user ON energy_records(user_id);

-- Device registration for ESP Oracle
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(64) UNIQUE NOT NULL,
    public_key VARCHAR(130) NOT NULL, -- 65 bytes uncompressed + 0x prefix
    owner_address VARCHAR(42) NOT NULL, -- User wallet that owns this device
    location_lat DECIMAL(10, 8),
    location_lon DECIMAL(11, 8),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'suspended', 'retired'
    last_seen TIMESTAMP,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy data submissions from devices
CREATE TABLE IF NOT EXISTS energy_submissions (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(64) REFERENCES devices(device_id) ON DELETE CASCADE,
    timestamp BIGINT NOT NULL,
    energy_kwh NUMERIC(20, 4) NOT NULL,
    signature VARCHAR(130) NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    submission_hash VARCHAR(66) UNIQUE, -- Prevent replay attacks
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for device queries
CREATE INDEX IF NOT EXISTS idx_devices_owner ON devices(owner_address);
CREATE INDEX IF NOT EXISTS idx_devices_status ON devices(status);
CREATE INDEX IF NOT EXISTS idx_submissions_device ON energy_submissions(device_id);
CREATE INDEX IF NOT EXISTS idx_submissions_timestamp ON energy_submissions(timestamp);
CREATE INDEX IF NOT EXISTS idx_submissions_hash ON energy_submissions(submission_hash) WHERE verified = FALSE;
