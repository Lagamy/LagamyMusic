import React, { useState, useEffect, useContext} from 'react';
import {MEDIA_URL} from '../serverConstants'
import '../styles/App.css';
import { styled } from '@mui/material/styles';
import {Link} from 'react-router-dom';
import MenuIcon from '@mui/icons-material/Menu';
import { AppBar, Typography, Button, IconButton, Box, Container, Avatar } from '@mui/material';
import { UserContext } from '../state_managment/userContext'
import { StyledToolbar } from '../theme';

const Logo = styled(Typography)(() => ({
  paddingBottom: "4px",
}));

const Header = () => {

  const { userState, logout } = useContext(UserContext);

  return ( <AppBar
  position="fixed"
  sx={{ boxShadow: 0, bgcolor: 'transparent', backgroundImage: 'none', mt: 5 }}
>
  <Container maxWidth="lg">
    <StyledToolbar variant="dense" disableGutters>
    <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', px: 0 }}>
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', alignItems: 'center' }}>
          <Logo variant='h5' className="Nav-link" id="Logo" component={Link} to="">
            Lagamy
          </Logo>
          <Typography className="Nav-link" component={Link} to="/artists">
            Artists
          </Typography>
          <Typography className="Nav-link" component={Link} to="/genres">
            Genres
          </Typography>
        </Box>
      </Box>
      <Box
        sx={{ // sx = vanilla css eddits
          display: { xs: 'none', md: 'flex' },
          gap: 1,
          alignItems: 'center',
        }}
      >
      {userState ? (
        <div>
          <Avatar alt={userState.username} src={MEDIA_URL + userState.image} component={Link} to={"/" + userState.id}/>
          <Button color="primary" variant="contained" size="small" onClick={logout}>
            Logout
          </Button>
        </div>
      ) : (
        <div>
          <Button color="primary" variant="text" size="small" component={Link} to="/login">
            Login
          </Button>
          <Button color="primary" variant="contained" size="small" component={Link} to="/register">
            Sign up
          </Button>
        </div>
       )}
      </Box>
      <Box sx={{ display: { sm: 'flex', md: 'none' } }}>
        <IconButton aria-label="Menu button">
          <MenuIcon />
        </IconButton>
      </Box>
    </StyledToolbar>
  </Container>
</AppBar>
);
}

export default Header