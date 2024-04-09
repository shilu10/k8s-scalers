import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './components/HomePage';
import AuthFormContainer from './components/AuthFormContainer'; // Your login page component
import { CssBaseline } from '@mui/material';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const accessToken = localStorage.getItem('accessToken');

  return (
    <Router>
      <ToastContainer />
      <CssBaseline />
      <Routes>
        <Route path="/login" element={<AuthFormContainer />} />
        <Route
          path="/"
          element={accessToken ? <HomePage /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
