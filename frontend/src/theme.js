import { createTheme } from '@mui/material';
import { orange } from '@mui/material/colors';
import { styled, alpha } from '@mui/material/styles';
import { Toolbar } from '@mui/material';

export const Theme = createTheme({
    palette: {
      mode: "dark",
      primary:{
        main: orange[500]
      }
    }
  });


export const StyledToolbar = styled(Toolbar)(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexShrink: 0,
    borderRadius: `calc(${theme.shape.borderRadius}px + 8px)`,
    backdropFilter: 'blur(24px)',
    border: '1px solid',
    borderColor: theme.palette.divider,
    backgroundColor: alpha(theme.palette.background.default, 0.2),
    boxShadow: theme.shadows[1],
    padding: '8px 12px',
  }));


  export const PlayerBar = styled(Toolbar)(({ theme }) => ({
    display: 'flex',
    justifyContent: 'center',
    flexShrink: 0,
    borderRadius: `calc(${theme.shape.borderRadius}px + 50px)`,
    backdropFilter: 'blur(24px)',
    border: '1px solid',
    borderColor: theme.palette.divider,
    backgroundColor: alpha(theme.palette.background.default, 0.2),
    boxShadow: theme.shadows[1],
    width: '70%',
    padding: '8px 12px',
  }));