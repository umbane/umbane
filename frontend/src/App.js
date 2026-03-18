import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { authService, tokenService } from './api';
import { POLYGON_CHAIN_ID } from './constants';
import './App.css';

const CONTRACT_ADDRESS = '0xF5D3E95244E07444eCFfE9BF04418cF1Fe398aDe';
const OWNER_ADDRESS = '0x5Ee264d83332Ba0Cf46f8b1EB7B064e34d62d7Dc';

function App() {
  const [connected, setConnected] = useState(false);
  const [address, setAddress] = useState('');
  const [balance, setBalance] = useState(null);
  const [totalSupply, setTotalSupply] = useState(null);
  const [loading, setLoading] = useState(false);
  const [operationLoading, setOperationLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [isOwner, setIsOwner] = useState(false);
  const [calcEnergy, setCalcEnergy] = useState('');
  const [calcResult, setCalcResult] = useState(null);

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
      setIsOwner(walletAddress.toLowerCase() === OWNER_ADDRESS.toLowerCase());
      
      try {
        await window.ethereum.request({
          method: 'wallet_watchAsset',
          params: {
            type: 'ERC20',
            options: {
              address: CONTRACT_ADDRESS,
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

  const addTokenToWallet = async () => {
    try {
      await window.ethereum.request({
        method: 'wallet_watchAsset',
        params: {
          type: 'ERC20',
          options: {
            address: CONTRACT_ADDRESS,
            symbol: 'UMB',
            decimals: 18,
          },
        },
      });
    } catch (e) {
      setStatus({ type: 'error', message: 'Failed to add token to wallet' });
    }
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
    setIsOwner(false);
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
      await fetchTotalSupply();
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
      await fetchTotalSupply();
    } catch (error) {
      setStatus({ type: 'error', message: error.response?.data?.error || error.message });
    }
    setOperationLoading(false);
  };

  const handleCalculate = async (e) => {
    e.preventDefault();
    if (!calcEnergy) return;
    
    setOperationLoading(true);
    try {
      const result = await tokenService.calculateCredits(calcEnergy);
      setCalcResult(result);
    } catch (error) {
      setStatus({ type: 'error', message: error.message });
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
              <button className="token-add-btn" onClick={addTokenToWallet}>
                + Add UMB to Wallet
              </button>
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
                <li><strong>Submit energy:</strong> Connect your solar panel or City Power feed-in meter data</li>
                <li><strong>Oracle verifies:</strong> Chainlink verifies your energy production (watts)</li>
                <li><strong>Tokens mint:</strong> UMB tokens minted to your wallet (1W = 1 UMB)</li>
                <li><strong>Trade carbon:</strong> Exchange UMB for carbon credits (aC) at trading desk</li>
                <li><strong>Earn rewards:</strong> Pledge tokens to earn CarB rewards</li>
              </ol>
            </div>

            <div className="calculator-section">
              <h4>Carbon Credit Calculator</h4>
              <p>Calculate how much you could earn from your energy production</p>
              <form onSubmit={handleCalculate} className="calculator-form">
                <input
                  type="number"
                  value={calcEnergy}
                  onChange={(e) => setCalcEnergy(e.target.value)}
                  placeholder="Energy production (kWh)"
                  min="0.001"
                  step="0.001"
                />
                <button type="submit" disabled={operationLoading}>
                  Calculate
                </button>
              </form>
              {calcResult && (
                <div className="calculator-result">
                  <div className="amount">{calcResult.credits} UMB</div>
                  <p>Based on {calcEnergy} kWh × carbon factor</p>
                </div>
              )}
            </div>

            {isOwner && (
              <div className="admin-section">
                <h4>🔧 Admin Panel</h4>
                <p>Contract owner functions</p>
                <div className="operations">
                  <div className="operation-card">
                    <h4>Mint Tokens</h4>
                    <p>Mint new UMB tokens to user wallets</p>
                    <form onSubmit={handleMint}>
                      <input
                        type="text"
                        name="address"
                        placeholder="Recipient address"
                        defaultValue={address}
                        required
                      />
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
              </div>
            )}

            <div className="info-section">
              <h4>Token System</h4>
              <div className="token-info">
                <div className="token-item">
                  <span className="token-name">mJ / UMB</span>
                  <span className="token-desc">Energy token - minted per watt of production. 1W = 1 UMB</span>
                </div>
                <div className="token-item">
                  <span className="token-name">aC</span>
                  <span className="token-desc">Carbon credit - obtained by exchanging UMB at trading desk</span>
                </div>
                <div className="token-item">
                  <span className="token-name">CarB</span>
                  <span className="token-desc">Pledge reward - created from UMB + aC, earns community rewards</span>
                </div>
              </div>
              <div className="links" style={{marginTop: '1rem'}}>
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
