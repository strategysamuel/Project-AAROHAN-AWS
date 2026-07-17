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
import { Download, Refresh, Gavel } from '@mui/icons-material';
import { apiUrl } from '../lib/api';
import { downloadFetchedFile, downloadTextFile } from '../lib/download';

const API = apiUrl('');

type Decision = {
  id: number;
  customer_id: number;
  recommendation: string;
  confidence_score: number;
  decision_score: number;
  risk_grade: string;
  approval_probability: number;
  eligible_loan_amount: number;
  recommended_product?: string | null;
  recommended_tenure: number;
  recommended_interest_rate: number;
  repayment_capacity: string;
  emi_estimate: number;
  debt_service_capacity: string;
  top_positive_factors: string[];
  top_negative_factors: string[];
  risk_drivers: string[];
  decision_explanation?: string | null;
  recommended_actions: string[];
  ai_narrative?: string | null;
  approval_status: string;
  policy_status: string;
  rbi_fraud_status?: string;
  created_at?: string;
};

const CreditDecisionPage: React.FC = () => {
  const [customerId, setCustomerId] = React.useState('99');
  const [loading, setLoading] = React.useState(false);
  const [decision, setDecision] = React.useState<Decision | null>(null);
  const [history, setHistory] = React.useState<Decision[]>([]);
  const [message, setMessage] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const loadDecision = React.useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [decisionRes, historyRes] = await Promise.all([
        fetch(`${API}/credit/decision/${customerId}`),
        fetch(`${API}/credit/history/${customerId}`)
      ]);

      setDecision(decisionRes.ok ? await decisionRes.json() : null);
      setHistory(historyRes.ok ? await historyRes.json() : []);
      if (!decisionRes.ok) {
        setMessage('No existing credit decision found. Generate one to create the first decision.');
      }
    } catch {
      setDecision(null);
      setHistory([]);
      setError('Credit engine unavailable.');
    } finally {
      setLoading(false);
    }
  }, [customerId]);

  React.useEffect(() => {
    loadDecision();
  }, [loadDecision]);

  const evaluate = async (refresh = false) => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const url = refresh ? `${API}/credit/refresh/${customerId}` : `${API}/credit/evaluate/${customerId}`;
      const response = await fetch(url, { method: 'POST' });
      if (!response.ok) {
        throw new Error('Credit decision request failed.');
      }

      setDecision(await response.json());
      await loadDecision();
      setMessage(refresh ? 'Credit decision refreshed.' : 'Credit decision generated.');
    } catch (exc: any) {
      setError(exc.message || 'Credit evaluation failed.');
    } finally {
      setLoading(false);
    }
  };

  const downloadExport = async (format: 'json' | 'pdf') => {
    try {
      if (format === 'json') {
        const response = await fetch(`${API}/credit/export/${customerId}?format=json`);
        if (!response.ok) throw new Error(`Export failed with status ${response.status}`);
        const payload = await response.json();
        downloadTextFile(`AAROHAN_CREDIT_DECISION_${customerId}.json`, JSON.stringify(payload, null, 2), 'application/json');
      } else {
        await downloadFetchedFile(`${API}/credit/export/${customerId}?format=pdf`, `AAROHAN_CREDIT_DECISION_${customerId}.pdf`);
      }
      setMessage(`Credit decision ${format.toUpperCase()} exported successfully.`);
    } catch (exc: any) {
      setError(exc.message || 'Credit export failed.');
    }
  };

  return (
    <Box sx={{ p: 1 }}>
      <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" spacing={2} sx={{ mb: 3 }}>
        <Box>
          <Typography variant="h5" fontWeight="bold">Credit Decision</Typography>
          <Typography variant="body2" color="text.secondary">
            Generate and review the AI credit underwriting decision.
          </Typography>
        </Box>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          <TextField size="small" label="Customer ID" value={customerId} onChange={(e) => setCustomerId(e.target.value)} sx={{ minWidth: 130 }} />
          <Button variant="outlined" startIcon={<Refresh />} onClick={() => evaluate(true)} disabled={loading}>Refresh</Button>
          <Button variant="contained" startIcon={<Gavel />} onClick={() => evaluate(false)} disabled={loading}>Evaluate</Button>
        </Stack>
      </Stack>

      {loading && <LinearProgress sx={{ mb: 2 }} />}
      {message && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage(null)}>{message}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="caption" color="text.secondary">Recommendation</Typography>
            <Typography variant="h4" fontWeight="bold" sx={{ mt: 1 }}>
              {decision?.recommendation || 'NA'}
            </Typography>
            <Chip label={decision?.risk_grade || 'UNKNOWN'} color={decision ? 'primary' : 'default'} sx={{ mt: 2 }} />
            <Divider sx={{ my: 2 }} />
            <Stack spacing={1.25}>
              <Button variant="outlined" startIcon={<Download />} onClick={() => downloadExport('json')} disabled={!decision}>Download JSON</Button>
              <Button variant="outlined" startIcon={<Download />} onClick={() => downloadExport('pdf')} disabled={!decision}>Download PDF</Button>
            </Stack>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Grid container spacing={2}>
            {[
              ['Confidence', decision ? `${decision.confidence_score.toFixed(1)}%` : 'NA'],
              ['Approval Probability', decision ? `${(decision.approval_probability * 100).toFixed(1)}%` : 'NA'],
              ['Loan Amount', decision ? `Rs ${decision.eligible_loan_amount.toLocaleString('en-IN')}` : 'NA'],
              ['Interest Rate', decision ? `${decision.recommended_interest_rate.toFixed(2)}%` : 'NA']
            ].map(([label, value]) => (
              <Grid item xs={6} md={3} key={label}>
                <Paper variant="outlined" sx={{ p: 2, height: '100%' }}>
                  <Typography variant="caption" color="text.secondary">{label}</Typography>
                  <Typography variant="body1" fontWeight="bold" sx={{ mt: 0.5 }}>{value}</Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>

          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', mt: 3 }}>
            <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>Decision Narrative</Typography>
            {!decision ? (
              <Alert severity="info">Evaluate a credit decision to inspect the lending narrative and factors.</Alert>
            ) : (
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="caption" color="text.secondary">Positive Factors</Typography>
                  <Stack spacing={1} sx={{ mt: 1 }}>
                    {decision.top_positive_factors.map((item) => <Chip key={item} label={item} variant="outlined" />)}
                  </Stack>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="caption" color="text.secondary">Negative Factors</Typography>
                  <Stack spacing={1} sx={{ mt: 1 }}>
                    {decision.top_negative_factors.map((item) => <Chip key={item} label={item} color="error" variant="outlined" />)}
                  </Stack>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="caption" color="text.secondary">Risk Drivers</Typography>
                  <Stack spacing={1} sx={{ mt: 1 }}>
                    {decision.risk_drivers.map((item) => <Chip key={item} label={item} color="warning" variant="outlined" />)}
                  </Stack>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="caption" color="text.secondary">Recommended Actions</Typography>
                  <Stack spacing={1} sx={{ mt: 1 }}>
                    {decision.recommended_actions.map((item) => <Chip key={item} label={item} color="primary" variant="outlined" />)}
                  </Stack>
                </Grid>
                <Grid item xs={12}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 1 }}>AI Narrative</Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap' }}>
                      {decision.ai_narrative || decision.decision_explanation || 'Not available'}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>Decision History</Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Created At</TableCell>
                    <TableCell>Recommendation</TableCell>
                    <TableCell>Risk Grade</TableCell>
                    <TableCell align="right">Confidence</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {history.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4}>No decision history yet.</TableCell>
                    </TableRow>
                  ) : (
                    history.map((item) => (
                      <TableRow key={item.id}>
                        <TableCell>{item.created_at ? new Date(item.created_at).toLocaleString() : 'NA'}</TableCell>
                        <TableCell>{item.recommendation}</TableCell>
                        <TableCell>{item.risk_grade}</TableCell>
                        <TableCell align="right">{item.confidence_score.toFixed(1)}%</TableCell>
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

export default CreditDecisionPage;