// src/utils/token.js

export const setTokens = (access, refresh) => {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
};

export const getAccessToken = () => {
  return localStorage.getItem("access");
};

export const clearTokens = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
