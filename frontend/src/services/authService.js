import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Register user
const register = async (userData) => {
  const response = await axios.post(`${API_URL}/auth/register`, userData);
  return response.data;
};

// Login user
const login = async (userData) => {
  const response = await axios.post(`${API_URL}/auth/login`, userData);
  return response.data;
};

// Logout user
const logout = async () => {
  localStorage.removeItem('token');
};

const authService = {
  register,
  login,
  logout,
};

export default authService;
