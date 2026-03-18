import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { authService, tokenService } from './api';
import { TOKEN_TYPES, POLYGON_CHAIN_ID } from './constants';
import './App.css';

function WalletConnect({ onConnect, connected, address }) {
  const [loading, setLoading] = useState(false);

  const connectWallet = async () => {
    if (!window.ethereum) {
      alert('Please install MetaMask!');
      return;
    }
    setLoading(true);
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const address = await signer.getAddress();
      
      const network = await provider.getNetwork();
      if (network.chainId !== parseInt(POLYGON_CHAIN_ID, 16)) {
        try {
          await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: POLYGON_CHAIN_ID }],
          });
        } catch (switchError) {
          alert('Please switch to Polygon Amoy network');
          setLoading(false);
          return;
        }
      }

      const message = 'Sign this message to authenticate with Umbane';
      const signature = await signer.signMessage(message);
      
      await authService.login(address, signature);
      onConnect(address);
    } catch (error) {
      console.error('Connection error:', error);
      alert('Failed to connect wallet');
    }
    setLoading(false);
  };

  if (connected) {
    return (
      <div className="wallet-connected">
        <span className="wallet-label">Connected:</span>
        <span className="wallet-address">{address.slice(0, 6)}...{address.slice(-4)}</span>
      </div>
    );
  }

  return (
    <button className="connect-btn" onClick={connectWallet} disabled={loading}>
      {loading ? 'Connecting...' : 'Connect Wallet'}
    </button>
  );
}

function BalanceDisplay({ address, balances, loading, onRefresh }) {
  return (
    <div className="balance-card">
      <h3>Token Balances</h3>
      <button className="refresh-btn" onClick={onRefresh} disabled={loading}>
        Refresh
      </button>
      <div className="balances">
        <div className="balance-item">
          <span className="token-label">mJ (Energy):</span>
          <span className="token-value">{balances.mJ || '0'}</span>
        </div>
        <div className="balance-item">
          <span className="token-label">aC (Carbon Credit):</span>
          <span className="token-value">{balances.aC || '0'}</span>
        </div>
      </div>
    </div>
  );
}

function TokenOperation({ operation, tokenType, onSubmit, loading }) {
  const [amount, setAmount] = useState('');
  const [recipient, setRecipient] = useState('');
  const [status, setStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    try {
      const data = operation === 'mint' 
        ? { address: recipient, amount }
        : { amount };
      await onSubmit(tokenType, data);
      setStatus({ success: true, message: `${operation.toUpperCase()} successful!` });
      setAmount('');
      setRecipient('');
    } catch (error) {
      setStatus({ success: false, message: error.response?.data?.error || error.message });
    }
  };

  return (
    <div className="operation-card">
      <h4>{operation === 'mint' ? 'Mint' : 'Burn'} {tokenType}</h4>
      <form onSubmit={handleSubmit}>
        {operation === 'mint' && (
          <input
            type="text"
            placeholder="Recipient address"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
          />
        )}
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          min="1"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : `${operation === 'mint' ? 'Mint' : 'Burn'} ${tokenType}`}
        </button>
      </form>
      {status && (
        <div className={`status ${status.success ? 'success' : 'error'}`}>
          {status.message}
        </div>
      )}
    </div>
  );
}

function TransactionHistory({ transactions }) {
  return (
    <div className="transactions-card">
      <h3>Transaction History</h3>
      {transactions.length === 0 ? (
        <p>No transactions yet</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Token</th>
              <th>Amount</th>
              <th>Tx Hash</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => (
              <tr key={tx.id}>
                <td>{tx.type}</td>
                <td>{tx.token_type}</td>
                <td>{tx.amount}</td>
                <td className="tx-hash">
                  <a 
                    href={`https://amoy.polygonscan.com/tx/${tx.tx_hash}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {tx.tx_hash?.slice(0, 10)}...
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

function App() {
  const [connected, setConnected] = useState(false);
  const [address, setAddress] = useState('');
  const [balances, setBalances] = useState({ mJ: null, aC: null });
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [operationLoading, setOperationLoading] = useState(false);

  useEffect(() => {
    const token = authService.getToken();
    const savedAddress = authService.getWalletAddress();
    if (token && savedAddress) {
      setConnected(true);
      setAddress(savedAddress);
    }
  }, []);

  useEffect(() => {
    if (connected && address) {
      fetchBalances();
      fetchTransactions();
    }
  }, [connected, address]);

  const fetchBalances = async () => {
    setLoading(true);
    try {
      const [mjBalance, acBalance] = await Promise.all([
        tokenService.getBalance(TOKEN_TYPES.MJ, address),
        tokenService.getBalance(TOKEN_TYPES.AC, address),
      ]);
      setBalances({
        mJ: mjBalance.balance,
        aC: acBalance.balance,
      });
    } catch (error) {
      console.error('Failed to fetch balances:', error);
    }
    setLoading(false);
  };

  const fetchTransactions = async () => {
    try {
      const data = await tokenService.getTransactions(address);
      setTransactions(data.transactions || []);
    } catch (error) {
      console.error('Failed to fetch transactions:', error);
    }
  };

  const handleMint = async (tokenType, data) => {
    setOperationLoading(true);
    try {
      if (tokenType === TOKEN_TYPES.MJ) {
        await tokenService.mintMJ(data.address, data.amount);
      } else {
        await tokenService.mintAC(data.address, data.amount);
      }
      await fetchBalances();
      await fetchTransactions();
    } finally {
      setOperationLoading(false);
    }
  };

  const handleBurn = async (tokenType, data) => {
    setOperationLoading(true);
    try {
      if (tokenType === TOKEN_TYPES.MJ) {
        await tokenService.burnMJ(data.amount);
      } else {
        await tokenService.burnAC(data.amount);
      }
      await fetchBalances();
      await fetchTransactions();
    } finally {
      setOperationLoading(false);
    }
  };

  const handleConnect = (walletAddress) => {
    setAddress(walletAddress);
    setConnected(true);
  };

  const handleDisconnect = () => {
    authService.logout();
    setConnected(false);
    setAddress('');
    setBalances({ mJ: null, aC: null });
    setTransactions([]);
  };

  return (
    <div className="App">
      <header>
        <h1>MECC Umbane Token System</h1>
        <div className="header-actions">
          {connected && (
            <button className="disconnect-btn" onClick={handleDisconnect}>
              Disconnect
            </button>
          )}
        </div>
      </header>

      <main>
        {!connected ? (
          <div className="connect-section">
            <p>Connect your wallet to interact with the Umbane token system</p>
            <WalletConnect onConnect={handleConnect} />
          </div>
        ) : (
          <>
            <div className="wallet-info">
              <WalletConnect 
                onConnect={handleConnect} 
                connected={connected} 
                address={address} 
              />
            </div>

            <BalanceDisplay 
              address={address}
              balances={balances}
              loading={loading}
              onRefresh={fetchBalances}
            />

            <div className="operations-grid">
              <TokenOperation 
                operation="mint"
                tokenType={TOKEN_TYPES.MJ}
                onSubmit={handleMint}
                loading={operationLoading}
              />
              <TokenOperation 
                operation="mint"
                tokenType={TOKEN_TYPES.AC}
                onSubmit={handleMint}
                loading={operationLoading}
              />
              <TokenOperation 
                operation="burn"
                tokenType={TOKEN_TYPES.MJ}
                onSubmit={handleBurn}
                loading={operationLoading}
              />
              <TokenOperation 
                operation="burn"
                tokenType={TOKEN_TYPES.AC}
                onSubmit={handleBurn}
                loading={operationLoading}
              />
            </div>

            <TransactionHistory transactions={transactions} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
