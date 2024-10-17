import React, { useState, useContext} from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import axios from 'axios';
import { UserContext } from '../state_managment/userContext'

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const server = 'http://127.0.0.1:8000'
  
  
  const { updateUser } = useContext(UserContext);

  // Handle form submit
  const postLogin = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    try {
      // Post login data to server
      const response = await axios.post(`${server}/login`, {
        username: username,
        password: password
      }, {
        withCredentials: true, // ensure cookies (JWT) are included in future requests
        headers: {
          'Content-Type': 'application/json', // Explicitly set Content-Type to JSON
        }
      }
    );
    await updateUser()
    console.log('Login successful:', response.data.message);
    // Handle login success (e.g., redirect or update state)
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed'); // Display error
    }
  };

  return (
    <Box component="form" onSubmit={postLogin} 
    sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2,
        mt: 5,
        maxWidth: '400px',
        mx: 'auto',
      }}
    >
      <Typography variant="h4" component="h1">
        Login
      </Typography>

      <TextField label="Username" variant="outlined" fullWidth value={username} onChange={(e) => setUsername(e.target.value)} required/>

      <TextField label="Password" type="password" variant="outlined" fullWidth value={password} onChange={(e) => setPassword(e.target.value)} required/>

      {error && (
        <Typography color="error" sx={{ mt: 1 }}>
          {error}
        </Typography>
      )}

      <Button type="submit" variant="contained" color="primary" fullWidth>
        Login
      </Button>
    </Box>
  );
};

export default Login;