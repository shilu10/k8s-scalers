// utils/auth.js
export const isTokenExpired = (token) => {
    if (!token) return true;
    const [, payload] = token.split('.');
    if (!payload) return true;
  
    try {
      const decoded = JSON.parse(atob(payload));
      const now = Math.floor(Date.now() / 1000);
      return decoded.exp < now;
    } catch {
      return true;
    }
  };
  