import {API_URL, MEDIA_URL} from '../serverConstants'
import React, { useState, useEffect, createContext} from 'react';
import axios from 'axios';
// Create Context
const UserContext = createContext();

// Create Provider Component
const UserProvider = ({ children }) => {
    const [error, setError] = useState(null); // State to track error
    const [userState, setUser] = useState(null)

    useEffect(() => {
        updateUser();
      }, []); 

      const logout = async () => {
        try {
          await axios.post(`${API_URL}/logout`, {}, { withCredentials: true });
          setUser(null);
        } catch (err) {
          setError(err.message);
        }
      };

      const updateUser = async () => {
        try {
          const response = await axios.get(`${API_URL}/user`, { withCredentials: true });
          setUser(response.data); 
        } catch (err) {
          setError(err.message); 
        }
      };

  return (
    <UserContext.Provider value={{ userState, setUser, updateUser, logout, error }}>
    {children}
    </UserContext.Provider>
  );
};

export { UserProvider, UserContext };