// AuthRoutes.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import AuthFormContainer from './components/AuthFormContainer';
import { useAuth } from './hooks/useAuth';
import { Box, CircularProgress } from '@mui/material';

const AuthRoutes = () => {
  const authReady = useAuth();

  if (!authReady) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Routes>
      <Route path="/login" element={<AuthFormContainer />} />
      <Route path="/" element={<HomePage />} />
    </Routes>
  );
};

export default AuthRoutes;
