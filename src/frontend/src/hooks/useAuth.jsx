import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { INGRESS_BASE_URL } from '../utils/config'; // adjust path if needed


export const useAuth = () => {
  const [authReady, setAuthReady] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    const isLoginPage = location.pathname === '/login';

    // Token expiry check
    const isAccessTokenExpired = () => {
      try {
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        return payload.exp * 1000 < Date.now();
      } catch {
        return true;
      }
    };

    const proceedToApp = async () => {
      if (!accessToken && !refreshToken) {
        if (!isLoginPage) navigate('/login');
        setAuthReady(true);
        return;
      }

      if (accessToken && !isAccessTokenExpired()) {
        setAuthReady(true);
        return;
      }

      // Access token expired, try refresh
      try {
        const res = await fetch(`${INGRESS_BASE_URL}/api/v1/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });

        if (!res.ok) throw new Error('Refresh failed');

        const data = await res.json();
        // Store new tokens
        localStorage.setItem('accessToken', data.data.access_token);
        localStorage.setItem('refreshToken', data.data.refresh_token);
        setAuthReady(true);
      } catch (err) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        navigate('/login');
        setAuthReady(true);
      }
    };

    proceedToApp();
  }, [location.pathname]);

  return authReady;
};
