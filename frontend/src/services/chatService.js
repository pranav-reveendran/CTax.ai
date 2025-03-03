import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const getAuthHeader = (token) => ({
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

// Create new conversation
const createConversation = async (conversationData, token) => {
  const response = await axios.post(
    `${API_URL}/chat/conversations`,
    conversationData,
    getAuthHeader(token)
  );
  return response.data.data;
};

// Get all conversations
const getConversations = async (token) => {
  const response = await axios.get(
    `${API_URL}/chat/conversations`,
    getAuthHeader(token)
  );
  return response.data.data;
};

// Get single conversation
const getConversation = async (conversationId, token) => {
  const response = await axios.get(
    `${API_URL}/chat/conversations/${conversationId}`,
    getAuthHeader(token)
  );
  return response.data.data;
};

// Send message
const sendMessage = async (conversationId, message, token) => {
  const response = await axios.post(
    `${API_URL}/chat/conversations/${conversationId}/messages`,
    { message },
    getAuthHeader(token)
  );
  return response.data.data;
};

// Delete conversation
const deleteConversation = async (conversationId, token) => {
  const response = await axios.delete(
    `${API_URL}/chat/conversations/${conversationId}`,
    getAuthHeader(token)
  );
  return response.data;
};

const chatService = {
  createConversation,
  getConversations,
  getConversation,
  sendMessage,
  deleteConversation,
};

export default chatService;
