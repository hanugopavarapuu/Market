import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

export interface PriceData {
  symbol: string;
  price: number;
  timestamp: string;
  provider: string;
}

export interface PollingJob {
  symbols: string[];
  interval: number;
  provider: string;
}

export interface PollingJobResponse {
  job_id: string;
  status: string;
  config: PollingJob;
}

const api = {
  getLatestPrice: async (symbol: string): Promise<PriceData> => {
    try {
      const response = await apiClient.get(`/prices/latest`, {
        params: { symbol },
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const message = error.response?.data?.detail || error.message;
        throw new Error(`Failed to fetch price: ${message}`);
      }
      throw error;
    }
  },

  createPollingJob: async (job: PollingJob): Promise<PollingJobResponse> => {
    try {
      const response = await apiClient.post('/prices/poll', job);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const message = error.response?.data?.detail || error.message;
        throw new Error(`Failed to create polling job: ${message}`);
      }
      throw error;
    }
  },
};

export default api; 