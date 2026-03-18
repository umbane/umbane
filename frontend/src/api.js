import axios from 'axios';
import { API_BASE_URL } from './constants';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: async (walletAddress, signature) => {
    const response = await api.post('/auth/login', {
      wallet_address: walletAddress,
      signature: signature
    });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('walletAddress', response.data.wallet_address);
    }
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('walletAddress');
  },
  getToken: () => localStorage.getItem('token'),
  getWalletAddress: () => localStorage.getItem('walletAddress'),
};

export const tokenService = {
  mintMJ: async (address, amount) => {
    const response = await api.post('/mintMJ', { address, amount });
    return response.data;
  },
  mintAC: async (address, amount) => {
    const response = await api.post('/mintAC', { address, amount });
    return response.data;
  },
  burnMJ: async (amount) => {
    const response = await api.post('/burnMJ', { amount });
    return response.data;
  },
  burnAC: async (amount) => {
    const response = await api.post('/burnAC', { amount });
    return response.data;
  },
  getBalance: async (tokenType, address) => {
    const response = await api.get(`/balance/${tokenType}/${address}`);
    return response.data;
  },
  getTransactions: async (address, limit = 50, offset = 0) => {
    const response = await api.get(`/transactions/${address}`, {
      params: { limit, offset }
    });
    return response.data;
  },
  setCarbonPrice: async (price) => {
    const response = await api.post('/chainlink/price-feed/set', { feed_address: price });
    return response.data;
  },
  getCarbonPrice: async () => {
    const response = await api.get('/chainlink/price-feed/get');
    return response.data;
  },
  calculateCredits: async (energyKwh) => {
    const response = await api.get('/chainlink/calculate-credits', {
      params: { energy_kwh: energyKwh }
    });
    return response.data;
  },
};

export const healthService = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  }
};

export default api;
