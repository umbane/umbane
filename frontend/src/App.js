import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { authService, tokenService } from './api';
import { POLYGON_CHAIN_ID } from './constants';
import './App.css';

function App() {
  const [connected, setConnected] = useState(false);
  const [address, setAddress] = useState('');
  const [balance, setBalance] = useState(null);
  const [totalSupply, setTotalSupply] = useState(null);
  const [loading, setLoading] = useState(false);
  const [operationLoading, setOperationLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const connectWallet = async () => {
    if (!window.ethereum) {
      alert('No wallet detected. Please install MetaMask.');
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
      
      try {
        await window.ethereum.request({
          method: 'wallet_watchAsset',
          params: {
            type: 'ERC20',
            options: {
              address: '0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe',
              symbol: 'UMB',
              decimals: 18,
            },
          },
        });
      } catch (e) {
        console.log('Token auto-add skipped');
      }
    } catch (error) {
      console.error('Connection error:', error);
      setStatus({ type: 'error', message: error.message || 'Failed to connect wallet' });
    }
    setLoading(false);
  };

  const disconnect = async () => {
    if (window.ethereum && typeof window.ethereum.disconnect === 'function') {
      try {
        await window.ethereum.disconnect();
      } catch (e) {
        console.log('Wallet disconnect not supported');
      }
    }
    authService.logout();
    localStorage.clear();
    sessionStorage.clear();
    setConnected(false);
    setAddress('');
    setBalance(null);
    setTotalSupply(null);
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

  const fetchTotalSupply = async () => {
    setLoading(true);
    try {
      const data = await tokenService.getTotalSupply();
      setTotalSupply(data.totalSupply);
    } catch (error) {
      console.error('Failed to fetch total supply:', error);
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
      fetchTotalSupply();
    }
  }, [connected, address]);

  const handleSubmitEnergy = async (e) => {
    e.preventDefault();
    const energyKwh = e.target.energyKwh.value;
    if (!energyKwh) return;

    setOperationLoading(true);
    setStatus(null);
    try {
      const credits = await tokenService.calculateCredits(energyKwh);
      setStatus({ 
        type: 'success', 
        message: `Based on ${energyKwh} kWh, you can earn ${credits.credits} UMB tokens. Submit to chain for verification.` 
      });
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
          <p className="subtitle">Carbon Credit System on Polygon Amoy</p>
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
            <p>Connect your wallet to earn carbon credits for your solar energy production</p>
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

            <div className="balances-grid">
              <div className="balance-card">
                <h3>Total Supply</h3>
                <div className="balance-amount">
                  {totalSupply ? parseInt(totalSupply).toLocaleString() : '0'}
                </div>
                <p className="balance-label">UMB tokens minted system-wide</p>
              </div>

              <div className="balance-card user-balance">
                <h3>Your Balance</h3>
                <div className="balance-amount">
                  {balance ? parseInt(balance).toLocaleString() : '0'}
                </div>
                <p className="balance-label">Your UMB tokens</p>
              </div>
            </div>

            {status && (
              <div className={`status ${status.type}`}>
                {status.message}
              </div>
            )}

            <div className="info-box">
              <h4>How It Works</h4>
              <ol>
                <li>Submit your energy production data (watts from solar/wind)</li>
                <li>Chainlink oracle verifies the data</li>
                <li>UMB tokens are minted to your wallet (1W = 1 UMB)</li>
                <li>Exchange UMB for carbon credits (aC) at trading desk</li>
                <li>Pledge tokens to earn CarB rewards</li>
              </ol>
            </div>

            <div className="operations">
              <div className="operation-card submit-energy">
                <h4>Submit Energy Production</h4>
                <p>Enter your energy production to calculate credits</p>
                <form onSubmit={handleSubmitEnergy}>
                  <input
                    type="number"
                    name="energyKwh"
                    placeholder="Energy (kWh)"
                    min="0.001"
                    step="0.001"
                    required
                  />
                  <button type="submit" disabled={operationLoading}>
                    {operationLoading ? 'Calculating...' : 'Calculate Credits'}
                  </button>
                </form>
              </div>
            </div>

            <div className="info-section">
              <h4>Token System</h4>
              <div className="token-info">
                <div className="token-item">
                  <span className="token-name">mJ / UMB</span>
                  <span className="token-desc">Energy token - minted per watt of production</span>
                </div>
                <div className="token-item">
                  <span className="token-name">aC</span>
                  <span className="token-desc">Carbon credit - obtained by exchanging UMB</span>
                </div>
                <div className="token-item">
                  <span className="token-name">CarB</span>
                  <span className="token-desc">Pledge reward - from UMB + aC</span>
                </div>
              </div>
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
