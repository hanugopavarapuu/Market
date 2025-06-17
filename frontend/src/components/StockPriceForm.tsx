import { useState } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Box,
  CircularProgress,
  useTheme,
  Alert,
  Autocomplete,
} from '@mui/material';
import api from '../services/api';
import type { PriceData } from '../services/api';

// Common stock symbols for quick selection
const COMMON_SYMBOLS = [
  'AAPL', // Apple
  'GOOGL', // Google
  'MSFT', // Microsoft
  'AMZN', // Amazon
  'META', // Meta (Facebook)
  'TSLA', // Tesla
  'NVDA', // NVIDIA
  'JPM', // JPMorgan Chase
  'V', // Visa
  'WMT', // Walmart
];

const StockPriceForm = () => {
  const [symbol, setSymbol] = useState('');
  const [priceData, setPriceData] = useState<PriceData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const theme = useTheme();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const trimmedSymbol = symbol.trim().toUpperCase();
      if (!trimmedSymbol) {
        throw new Error('Please enter a stock symbol');
      }

      // Basic validation for stock symbol format
      if (!/^[A-Z]{1,5}$/.test(trimmedSymbol)) {
        throw new Error('Invalid stock symbol format. Please use 1-5 uppercase letters.');
      }

      const data = await api.getLatestPrice(trimmedSymbol);
      setPriceData(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch price data';
      setError(errorMessage);
      setPriceData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      sx={{
        background: theme.palette.mode === 'dark'
          ? 'linear-gradient(145deg, #1E1E1E 0%, #2D2D2D 100%)'
          : 'linear-gradient(145deg, #FFFFFF 0%, #F5F5F5 100%)',
        border: `1px solid ${theme.palette.mode === 'dark' ? '#333' : '#E0E0E0'}`,
      }}
    >
      <CardContent>
        <Typography variant="h2" gutterBottom className="gradient-text">
          Get Latest Price
        </Typography>
        <form onSubmit={handleSubmit}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 3 }}>
            <Autocomplete
              freeSolo
              options={COMMON_SYMBOLS}
              value={symbol}
              onChange={(_, newValue) => setSymbol(newValue || '')}
              onInputChange={(_, newInputValue) => setSymbol(newInputValue.toUpperCase())}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Stock Symbol"
                  placeholder="e.g., AAPL"
                  required
                  error={!!error}
                  helperText={error || "Enter a valid stock symbol"}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      '&:hover fieldset': {
                        borderColor: theme.palette.primary.main,
                      },
                    },
                  }}
                />
              )}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
              sx={{ minWidth: 120, alignSelf: 'flex-end' }}
            >
              {loading ? <CircularProgress size={24} /> : 'Fetch'}
            </Button>
          </Box>
        </form>

        {error && (
          <Alert 
            severity="error" 
            sx={{ 
              mt: 2,
              animation: 'fadeIn 0.3s ease-in-out',
            }}
          >
            {error}
          </Alert>
        )}

        {priceData && (
          <Box 
            sx={{ 
              mt: 3,
              animation: 'fadeIn 0.5s ease-in-out',
              background: theme.palette.mode === 'dark'
                ? 'linear-gradient(145deg, #2D2D2D 0%, #1E1E1E 100%)'
                : 'linear-gradient(145deg, #F5F5F5 0%, #FFFFFF 100%)',
              p: 2,
              borderRadius: 1,
            }}
          >
            <Typography variant="h3" gutterBottom className="gradient-text">
              {priceData.symbol}
            </Typography>
            <Typography 
              variant="h4" 
              sx={{ 
                color: theme.palette.primary.main,
                fontWeight: 'bold',
                mb: 2,
              }}
            >
              ${priceData.price.toFixed(2)}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Last updated: {new Date(priceData.timestamp).toLocaleString()}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Provider: {priceData.provider}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default StockPriceForm; 