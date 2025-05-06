import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchAnalysis = async (code: string) => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await axios.post(
      `${API_URL}/analyze`,
      { code },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;
  } catch (error) {
    console.error('Error analyzing code:', error);
    throw error;
  }
};