import React, { useState } from 'react';
import { Button, Box, CircularProgress } from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import FormField from './FormField';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom'; // useNavigate for redirection

export default function AuthForm({ isLogin, onToggleLogin }) {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); // useNavigate hook for redirection

  const validationSchema = Yup.object({
    email: Yup.string().email('Invalid email').required('Email required'),
    password: Yup.string().min(6, 'Min 6 chars').required('Password required'),
    ...(isLogin
      ? {}
      : {
          confirmPassword: Yup.string()
            .oneOf([Yup.ref('password')], 'Passwords must match')
            .required('Confirm your password'),
        }),
  });

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
    validationSchema,
    onSubmit: async (values) => {
      setLoading(true);
      try {
        const url = isLogin
          ? 'http://localhost:8000/api/v1/login'
          : 'http://localhost:8000/api/v1/register';

        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: values.email,
            password: values.password,
          }),
        });

        const data = await response.json();
        console.log(data);

        if (data.success) {
          // ✅ Store tokens if available
          if (data.data.access_token) {
            const accessToken = data.data.access_token;
            localStorage.setItem('accessToken', accessToken);
          }
          if (data.data.refresh_token) {
            const refreshToken = data.data.refresh_token;
            localStorage.setItem('refreshToken', refreshToken);
          }

          toast.success(isLogin ? 'Login Successful!' : 'Signup Successful!');

          // Redirect to home page directly after successful login/signup
          if (isLogin) {
            navigate('/'); // This ensures the user is redirected to the homepage
          } else if (!isLogin && data.success && onToggleLogin) {
            onToggleLogin(); // Switch the form mode to login after successful signup
          }
        } else {
          toast.error(data.error || 'Something went wrong');
        }
      } catch (error) {
        toast.error('An error occurred. Please try again.');
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} noValidate>
      <FormField label="Email" name="email" type="email" formik={formik} />
      <FormField label="Password" name="password" type="password" formik={formik} />
      {!isLogin && (
        <FormField
          label="Confirm Password"
          name="confirmPassword"
          type="password"
          formik={formik}
        />
      )}
      <Box mt={2}>
        <Button
          type="submit"
          fullWidth
          variant="contained"
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : isLogin ? 'Login' : 'Sign Up'}
        </Button>
      </Box>
    </form>
  );
}
