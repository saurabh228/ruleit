import axios from 'axios';

// Base URL configuration
const apiClient = axios.create({
  // baseURL: process.env.REACT_APP_API_URL,
  baseURL: 'http://localhost:8000/',
  headers: {
    'Content-Type': 'application/json',
  },
});


// API call to create a single rule
export const createRule = (ruleData) => {
  return apiClient.post('/api/create-rule/', ruleData);
};

// API call to get all rules
export const getRules = (page) => {
  return apiClient.get(`/api/rules/?page=${page}`);
};

// API call to get a single rule
export const getRule = (ruleId) => {
  return apiClient.get(`/api/rules/${ruleId}/`);
};

// API call to edit a rule
export const editRule = (ruleData) => {
  return apiClient.post('/api/edit-rule/', ruleData);
};

// API call to evaluate a rule
export const evaluateRule = (ruleData) => {
  return apiClient.post('/api/evaluate-rule/', ruleData);
}; 

// API call to combine multiple rules
export const combineRules = (combinedData) => {
  return apiClient.post('/api/combine-rules/', combinedData);
};

export default apiClient;