import React, { useState } from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import AuthForm from './AuthForm';

const MotionPaper = motion(Paper);

export default function AuthFormContainer() {
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate(); // Hook for navigation

  const toggleMode = () => setIsLogin((prev) => !prev);

  // Callback function to be called on successful login
  const onLoginSuccess = () => {
    // Navigate to home page after successful login
    navigate('/');
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      bgcolor="#f5f5f5"
    >
      <MotionPaper
        elevation={4}
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        sx={{
          width: 400,
          padding: 4,
          borderRadius: 3,
          backgroundColor: 'white',
        }}
      >
        <Typography variant="h5" align="center" mb={3}>
          {isLogin ? 'Login' : 'Sign Up'}
        </Typography>

        {/* 🔥 Pass onLoginSuccess to AuthForm */}
        <AuthForm
          key={isLogin ? 'login' : 'signup'}
          isLogin={isLogin}
          onToggleLogin={() => setIsLogin(true)} // switches to login on signup success
          onLoginSuccess={onLoginSuccess} // Pass the success handler to AuthForm
        />

        <Button onClick={toggleMode} fullWidth sx={{ mt: 2 }}>
          {isLogin
            ? "Don't have an account? Sign up"
            : 'Already have an account? Login'}
        </Button>
      </MotionPaper>
    </Box>
  );
}
