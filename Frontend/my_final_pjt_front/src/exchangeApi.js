import axios from 'axios';

const BASE_URL = 'http://localhost:8000/exchange';

export const getExchangeRates = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/rates/`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch exchange rates:', error);
    throw error;
  }
};
