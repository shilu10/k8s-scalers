import React, { useState } from 'react';
import { Button, Box, CircularProgress } from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import FormField from './FormField';

export default function AuthForm({ isLogin }) {
  const [loading, setLoading] = useState(false);

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
      await new Promise((r) => setTimeout(r, 1500)); // simulate API
      alert(JSON.stringify(values, null, 2));
      setLoading(false);
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} noValidate>
      <FormField
        label="Email"
        name="email"
        type="email"
        formik={formik}
      />
      <FormField
        label="Password"
        name="password"
        type="password"
        formik={formik}
      />
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
