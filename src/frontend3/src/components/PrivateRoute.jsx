import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ element, ...rest }) => {
  const accessToken = localStorage.getItem('accessToken');
  
  // If the user is not logged in, redirect to login page
  if (!accessToken) {
    return <Navigate to="/login" />;
  }
  
  return <Route {...rest} element={element} />;
};

export default PrivateRoute;
