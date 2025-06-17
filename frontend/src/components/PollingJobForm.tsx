import { useState } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Box,
  CircularProgress,
  Chip,
  useTheme,
} from '@mui/material';
import api from '../services/api';
import type { PollingJobResponse } from '../services/api';

const PollingJobForm = () => {
  const [symbols, setSymbols] = useState('');
  const [interval, setInterval] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [jobResponse, setJobResponse] = useState<PollingJobResponse | null>(null);
  const theme = useTheme();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const symbolList = symbols
        .split(',')
        .map((s) => s.trim().toUpperCase())
        .filter(Boolean);

      if (symbolList.length === 0) {
        throw new Error('Please enter at least one symbol');
      }

      const response = await api.createPollingJob({
        symbols: symbolList,
        interval: parseInt(interval, 10),
        provider: 'yfinance',
      });

      setJobResponse(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create polling job');
      setJobResponse(null);
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
          Create Polling Job
        </Typography>
        <form onSubmit={handleSubmit}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              label="Stock Symbols"
              value={symbols}
              onChange={(e) => setSymbols(e.target.value)}
              placeholder="e.g., AAPL, GOOGL, MSFT"
              required
              helperText="Enter symbols separated by commas"
              sx={{
                '& .MuiOutlinedInput-root': {
                  '&:hover fieldset': {
                    borderColor: theme.palette.primary.main,
                  },
                },
              }}
            />
            <TextField
              fullWidth
              label="Interval (seconds)"
              type="number"
              value={interval}
              onChange={(e) => setInterval(e.target.value)}
              placeholder="e.g., 60"
              required
              inputProps={{ min: 1 }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '&:hover fieldset': {
                    borderColor: theme.palette.primary.main,
                  },
                },
              }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
              sx={{ mt: 2 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Create Job'}
            </Button>
          </Box>
        </form>

        {error && (
          <Typography 
            color="error" 
            sx={{ 
              mt: 2,
              animation: 'fadeIn 0.3s ease-in-out',
            }}
          >
            {error}
          </Typography>
        )}

        {jobResponse && (
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
              Job Created
            </Typography>
            <Typography variant="body1" gutterBottom>
              Job ID: {jobResponse.job_id}
            </Typography>
            <Typography variant="body1" gutterBottom>
              Status: {jobResponse.status}
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1" gutterBottom>
                Symbols:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {jobResponse.config.symbols.map((symbol) => (
                  <Chip 
                    key={symbol} 
                    label={symbol}
                    sx={{
                      background: theme.palette.mode === 'dark'
                        ? 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)'
                        : 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                      color: 'white',
                    }}
                  />
                ))}
              </Box>
            </Box>
            <Typography variant="body1" sx={{ mt: 2 }}>
              Interval: {jobResponse.config.interval} seconds
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default PollingJobForm; 