// App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { CssBaseline } from '@mui/material';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AuthRoutes from './AuthRoutes';

function App() {
  return (
    <Router>
      <ToastContainer />
      <CssBaseline />
      <AuthRoutes />
    </Router>
  );
}

export default App;
