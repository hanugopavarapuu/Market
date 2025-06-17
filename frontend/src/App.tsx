import { useState, useMemo } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Container, Box, Typography, IconButton, useMediaQuery } from '@mui/material';
import { lightTheme, darkTheme } from './theme';
import StockPriceForm from './components/StockPriceForm';
import PollingJobForm from './components/PollingJobForm';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const [mode, setMode] = useState<'light' | 'dark'>(prefersDarkMode ? 'dark' : 'light');

  const theme = useMemo(() => (mode === 'light' ? lightTheme : darkTheme), [mode]);

  const toggleColorMode = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ py: 8 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
            <Typography variant="h1" component="h1">
              Market Data Service
            </Typography>
            <IconButton onClick={toggleColorMode} color="inherit" sx={{ ml: 2 }}>
              {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Box>
          <Box 
            sx={{ 
              display: 'grid', 
              gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, 
              gap: 4, 
              mt: 4,
              '& > *': {
                animation: 'fadeIn 0.5s ease-in-out',
              },
            }}
          >
            <StockPriceForm />
            <PollingJobForm />
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
