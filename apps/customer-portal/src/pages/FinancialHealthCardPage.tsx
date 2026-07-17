import React from 'react';
import {
  Alert,
  Box,
  Button,
  Chip,
  Divider,
  Grid,
  LinearProgress,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography
} from '@mui/material';
import { Assessment, Download, Refresh } from '@mui/icons-material';
import { apiUrl } from '../lib/api';
import { downloadFetchedFile, downloadTextFile } from '../lib/download';

const API = apiUrl('');

type FhcCard = {
  customer_id: number;
  overall_score: number;
  rating: string;
  key_strengths?: string | null;
  risk_concerns?: string | null;
  ai_explanation?: string | null;
  updated_at?: string;
};

const FinancialHealthCardPage: React.FC = () => {
  const [customerId, setCustomerId] = React.useState('99');
  const [loading, setLoading] = React.useState(false);
  const [card, setCard] = React.useState<FhcCard | null>(null);
  const [history, setHistory] = React.useState<Array<{ recorded_at: string; score_value: number; rating: string }>>([]);
  const [message, setMessage] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const loadCard = React.useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [cardRes, historyRes] = await Promise.all([
        fetch(`${API}/fhc/${customerId}`),
        fetch(`${API}/fhc/history/${customerId}`)
      ]);

      setCard(cardRes.ok ? await cardRes.json() : null);
      setHistory(historyRes.ok ? await historyRes.json() : []);
      if (!cardRes.ok) {
        setMessage('No existing FHC found. Generate one to create the first score.');
      }
    } catch {
      setCard(null);
      setHistory([]);
      setError('FHC service unavailable.');
    } finally {
      setLoading(false);
    }
  }, [customerId]);

  React.useEffect(() => {
    loadCard();
  }, [loadCard]);

  const generate = async (refresh = false) => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const url = refresh ? `${API}/fhc/refresh/${customerId}` : `${API}/fhc/calculate/${customerId}`;
      const response = await fetch(url, { method: 'POST' });
      if (!response.ok) {
        throw new Error('FHC generation failed.');
      }

      setCard(await response.json());
      await loadCard();
      setMessage(refresh ? 'Financial Health Card refreshed.' : 'Financial Health Card generated.');
    } catch (exc: any) {
      setError(exc.message || 'FHC generation failed.');
    } finally {
      setLoading(false);
    }
  };

  const downloadExport = async (format: 'json' | 'pdf') => {
    try {
      if (format === 'json') {
        const response = await fetch(`${API}/fhc/export/${customerId}?format=json`);
        if (!response.ok) throw new Error(`Export failed with status ${response.status}`);
        const payload = await response.json();
        downloadTextFile(`AAROHAN_FHC_${customerId}.json`, JSON.stringify(payload, null, 2), 'application/json');
      } else {
        await downloadFetchedFile(`${API}/fhc/export/${customerId}?format=pdf`, `AAROHAN_FHC_${customerId}.pdf`);
      }
      setMessage(`FHC ${format.toUpperCase()} exported successfully.`);
    } catch (exc: any) {
      setError(exc.message || 'FHC export failed.');
    }
  };

  return (
    <Box sx={{ p: 1 }}>
      <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" spacing={2} sx={{ mb: 3 }}>
        <Box>
          <Typography variant="h5" fontWeight="bold">Financial Health Card</Typography>
          <Typography variant="body2" color="text.secondary">
            Generate, refresh, and export the enterprise financial health score.
          </Typography>
        </Box>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          <TextField size="small" label="Customer ID" value={customerId} onChange={(e) => setCustomerId(e.target.value)} sx={{ minWidth: 130 }} />
          <Button variant="outlined" startIcon={<Refresh />} onClick={() => generate(true)} disabled={loading}>Refresh</Button>
          <Button variant="contained" startIcon={<Assessment />} onClick={() => generate(false)} disabled={loading}>Generate FHC</Button>
        </Stack>
      </Stack>

      {loading && <LinearProgress sx={{ mb: 2 }} />}
      {message && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage(null)}>{message}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="caption" color="text.secondary">Current Score</Typography>
            <Typography variant="h3" fontWeight="bold" sx={{ mt: 1 }}>
              {card ? card.overall_score.toFixed(1) : 'NA'}
            </Typography>
            <Chip label={card?.rating || 'NOT GENERATED'} color={card ? 'primary' : 'default'} sx={{ mt: 2 }} />
            <Divider sx={{ my: 2 }} />
            <Stack spacing={1.25}>
              <Button variant="outlined" startIcon={<Download />} onClick={() => downloadExport('json')} disabled={!card}>Download JSON</Button>
              <Button variant="outlined" startIcon={<Download />} onClick={() => downloadExport('pdf')} disabled={!card}>Download PDF</Button>
            </Stack>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>Score Detail</Typography>
            {!card ? (
              <Alert severity="info">Generate a card to inspect scores, strengths, and risk explanations.</Alert>
            ) : (
              <Grid container spacing={2}>
                {[
                  ['Overall Score', card.overall_score],
                  ['Rating', card.rating],
                  ['Strengths', card.key_strengths || 'N/A'],
                  ['Risk Concerns', card.risk_concerns || 'N/A'],
                  ['AI Explanation', card.ai_explanation || 'N/A']
                ].map(([label, value]) => (
                  <Grid item xs={12} sm={6} key={label as string}>
                    <Paper variant="outlined" sx={{ p: 2, height: '100%' }}>
                      <Typography variant="caption" color="text.secondary">{label}</Typography>
                      <Typography variant="body1" fontWeight="bold" sx={{ mt: 0.5 }}>
                        {typeof value === 'number' ? value.toFixed(1) : value}
                      </Typography>
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>Score History</Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Recorded At</TableCell>
                    <TableCell>Score</TableCell>
                    <TableCell>Rating</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {history.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={3}>No score history yet.</TableCell>
                    </TableRow>
                  ) : (
                    history.map((item, index) => (
                      <TableRow key={`${item.recorded_at}-${index}`}>
                        <TableCell>{new Date(item.recorded_at).toLocaleString()}</TableCell>
                        <TableCell>{item.score_value.toFixed(1)}</TableCell>
                        <TableCell>{item.rating}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default FinancialHealthCardPage;