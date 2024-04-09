import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

export const useAuth = () => {
  const [authReady, setAuthReady] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    const isLoginPage = location.pathname === '/login';

    if (!accessToken && !refreshToken) {
      // User is not logged in, allow login page
      if (!isLoginPage) {
        navigate('/login');
      }
      setAuthReady(true);
      return;
    }

    const isAccessTokenExpired = () => {
      try {
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        return payload.exp * 1000 < Date.now();
      } catch {
        return true;
      }
    };

    const refreshTokenFn = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/refresh', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refreshToken }),
        });

        if (!res.ok) throw new Error('Refresh failed');

        const data = await res.json();
        localStorage.setItem('accessToken', data.accessToken);
        setAuthReady(true);
      } catch (err) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        navigate('/login');
        setAuthReady(true); // Still allow rendering to prevent blank page
      }
    };

    if (isAccessTokenExpired()) {
      refreshTokenFn();
    } else {
      setAuthReady(true);
    }
  }, [navigate, location]);

  return authReady;
};
