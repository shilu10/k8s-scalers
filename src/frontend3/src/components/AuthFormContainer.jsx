import React, { useState } from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { motion } from 'framer-motion';
import AuthForm from './AuthForm';

const MotionPaper = motion(Paper);

export default function AuthFormContainer() {
  const [isLogin, setIsLogin] = useState(true);

  const toggleMode = () => setIsLogin((prev) => !prev);

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

        <AuthForm isLogin={isLogin} />

        <Button onClick={toggleMode} fullWidth sx={{ mt: 2 }}>
          {isLogin
            ? "Don't have an account? Sign up"
            : 'Already have an account? Login'}
        </Button>
      </MotionPaper>
    </Box>
  );
}
