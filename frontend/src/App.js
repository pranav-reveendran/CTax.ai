import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { Box } from '@mui/material';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Navbar from './components/Navbar';

function App() {
  const { token } = useSelector((state) => state.auth);

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {token && <Navbar />}
      <Routes>
        <Route
          path="/login"
          element={!token ? <Login /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/register"
          element={!token ? <Register /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/dashboard"
          element={token ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/chat/:id"
          element={token ? <Chat /> : <Navigate to="/login" />}
        />
        <Route
          path="/"
          element={<Navigate to={token ? '/dashboard' : '/login'} />}
        />
      </Routes>
    </Box>
  );
}

export default App;
