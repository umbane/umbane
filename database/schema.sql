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
