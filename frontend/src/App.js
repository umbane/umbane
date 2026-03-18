import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { authService, tokenService } from './api';
import { POLYGON_CHAIN_ID } from './constants';
import './App.css';

function App() {
  const [connected, setConnected] = useState(false);
  const [address, setAddress] = useState('');
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [operationLoading, setOperationLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const connectWallet = async () => {
    if (!window.ethereum) {
      alert('Please install MetaMask!');
      return;
    }
    setLoading(true);
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const walletAddress = await signer.getAddress();
      
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
      
      await authService.login(walletAddress, signature);
      setAddress(walletAddress);
      setConnected(true);
    } catch (error) {
      console.error('Connection error:', error);
      setStatus({ type: 'error', message: 'Failed to connect wallet' });
    }
    setLoading(false);
  };

  const disconnect = () => {
    authService.logout();
    setConnected(false);
    setAddress('');
    setBalance(null);
    setStatus(null);
  };

  const fetchBalance = async () => {
    if (!address) return;
    setLoading(true);
    try {
      const data = await tokenService.getBalance('mJ', address);
      setBalance(data.balance);
    } catch (error) {
      console.error('Failed to fetch balance:', error);
    }
    setLoading(false);
  };

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
      fetchBalance();
    }
  }, [connected, address]);

  const handleMint = async (e) => {
    e.preventDefault();
    const amount = e.target.amount.value;
    if (!amount) return;

    setOperationLoading(true);
    setStatus(null);
    try {
      await tokenService.mintMJ(address, amount);
      setStatus({ type: 'success', message: `Minted ${amount} UMB tokens!` });
      await fetchBalance();
    } catch (error) {
      setStatus({ type: 'error', message: error.response?.data?.error || error.message });
    }
    setOperationLoading(false);
  };

  const handleBurn = async (e) => {
    e.preventDefault();
    const amount = e.target.amount.value;
    if (!amount) return;

    setOperationLoading(true);
    setStatus(null);
    try {
      await tokenService.burnMJ(amount);
      setStatus({ type: 'success', message: `Burned ${amount} UMB tokens!` });
      await fetchBalance();
    } catch (error) {
      setStatus({ type: 'error', message: error.response?.data?.error || error.message });
    }
    setOperationLoading(false);
  };

  return (
    <div className="App">
      <header>
        <div className="header-content">
          <h1>🌱 Umbane Token</h1>
          <p className="subtitle">Carbon Credit System on Polygon</p>
        </div>
        {connected && (
          <button className="disconnect-btn" onClick={disconnect}>
            Disconnect
          </button>
        )}
      </header>

      <main>
        {!connected ? (
          <div className="connect-section">
            <div className="logo">🌍</div>
            <h2>Welcome to Umbane</h2>
            <p>Connect your wallet to start trading carbon credits on Polygon Amoy</p>
            <div className="network-badge">Polygon Amoy Testnet</div>
            <button className="connect-btn" onClick={connectWallet} disabled={loading}>
              {loading ? 'Connecting...' : 'Connect Wallet'}
            </button>
          </div>
        ) : (
          <div className="dashboard">
            <div className="wallet-info">
              <span className="wallet-label">Wallet:</span>
              <span className="wallet-address">{address.slice(0, 6)}...{address.slice(-4)}</span>
            </div>

            <div className="balance-card">
              <h3>Your UMB Balance</h3>
              <div className="balance-amount">
                {balance ? parseInt(balance).toLocaleString() : '0'}
              </div>
              <button className="refresh-btn" onClick={fetchBalance} disabled={loading}>
                Refresh
              </button>
            </div>

            {status && (
              <div className={`status ${status.type}`}>
                {status.message}
              </div>
            )}

            <div className="operations">
              <div className="operation-card">
                <h4>Mint Tokens</h4>
                <p>Mint new UMB tokens (owner only)</p>
                <form onSubmit={handleMint}>
                  <input
                    type="number"
                    name="amount"
                    placeholder="Amount"
                    min="1"
                    required
                  />
                  <button type="submit" disabled={operationLoading}>
                    {operationLoading ? 'Minting...' : 'Mint UMB'}
                  </button>
                </form>
              </div>

              <div className="operation-card">
                <h4>Burn Tokens</h4>
                <p>Burn UMB tokens to reduce supply</p>
                <form onSubmit={handleBurn}>
                  <input
                    type="number"
                    name="amount"
                    placeholder="Amount"
                    min="1"
                    required
                  />
                  <button type="submit" disabled={operationLoading}>
                    {operationLoading ? 'Burning...' : 'Burn UMB'}
                  </button>
                </form>
              </div>
            </div>

            <div className="info-section">
              <h4>About Umbane</h4>
              <p>
                Umbane is a carbon credit token system built on Polygon Amoy with Chainlink oracle integration.
                Track energy usage and mint carbon credits dynamically.
              </p>
              <div className="links">
                <a href="https://amoy.polygonscan.com/token/0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe" target="_blank" rel="noopener noreferrer">
                  View Contract ↗
                </a>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
