/**
 * Application constants
 */

export const VISA_TYPES = [
  { value: 'F-1', label: 'F-1 Student Visa' },
  { value: 'J-1', label: 'J-1 Exchange Visitor' },
  { value: 'H-1B', label: 'H-1B Work Visa' },
  { value: 'OPT', label: 'Optional Practical Training (OPT)' },
  { value: 'CPT', label: 'Curricular Practical Training (CPT)' },
  { value: 'Other', label: 'Other' },
];

export const TAX_YEARS = [2024, 2023, 2022, 2021, 2020];

export const MESSAGE_ROLES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system',
};

export const API_STATUS = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error',
};

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  CHAT: '/chat',
};

export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  AUTH_FAILED: 'Authentication failed. Please try again.',
  SERVER_ERROR: 'Server error. Please try again later.',
  INVALID_INPUT: 'Invalid input. Please check your data.',
};
