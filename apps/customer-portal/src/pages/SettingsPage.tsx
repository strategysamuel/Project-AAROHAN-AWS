import React from 'react';
import {
  Alert,
  Box,
  Button,
  Divider,
  Grid,
  LinearProgress,
  MenuItem,
  Paper,
  Stack,
  Tab,
  Tabs,
  TextField,
  Typography
} from '@mui/material';
import { Refresh, Save } from '@mui/icons-material';
import { apiUrl } from '../lib/api';

const API = apiUrl('');

const ADAPTER_OPTIONS = ['RULE_ENGINE', 'VERTEX_AI', 'CUSTOM_ML', 'OPENAI_LLM'];

const toPrettyJson = (value: unknown): string => JSON.stringify(value, null, 2);

const SettingsPage: React.FC = () => {
  const [tab, setTab] = React.useState(0);
  const [loading, setLoading] = React.useState(false);
  const [message, setMessage] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const [creditAdapter, setCreditAdapter] = React.useState('RULE_ENGINE');
  const [creditRuleParameters, setCreditRuleParameters] = React.useState('{\n  "fhc_score_threshold": 85.0,\n  "dscr_threshold": 1.2,\n  "gst_delay_threshold": 10\n}');
  const [creditRiskThresholds, setCreditRiskThresholds] = React.useState('{\n  "Low": 80.0,\n  "Medium": 60.0,\n  "High": 40.0,\n  "Critical": 0.0\n}');

  const [fhcWeights, setFhcWeights] = React.useState('{\n  "identity_weight": 0.10,\n  "compliance_weight": 0.12,\n  "liquidity_weight": 0.10\n}');
  const [fhcThresholds, setFhcThresholds] = React.useState('{\n  "AAA": 85.0,\n  "AA": 75.0,\n  "A": 65.0,\n  "BBB": 55.0\n}');

  const [fraudAdapter, setFraudAdapter] = React.useState('RULE_ENGINE');
  const [fraudRuleParameters, setFraudRuleParameters] = React.useState('{\n  "watchlist_threshold": 0.8,\n  "override_threshold": 0.5\n}');

  const loadSettings = React.useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [creditRes, fhcRes, fraudRes] = await Promise.all([
        fetch(`${API}/credit/config`),
        fetch(`${API}/fhc/config`),
        fetch(`${API}/rbi/config`)
      ]);

      if (creditRes.ok) {
        const payload = await creditRes.json();
        setCreditAdapter(payload.active_adapter || 'RULE_ENGINE');
        setCreditRuleParameters(toPrettyJson(payload.rule_parameters || {}));
        setCreditRiskThresholds(toPrettyJson(payload.risk_thresholds || {}));
      }

      if (fhcRes.ok) {
        const payload = await fhcRes.json();
        setFhcWeights(toPrettyJson(payload.weights || {}));
        setFhcThresholds(toPrettyJson(payload.thresholds || {}));
      }

      if (fraudRes.ok) {
        const payload = await fraudRes.json();
        setFraudAdapter(payload.active_adapter || 'RULE_ENGINE');
        setFraudRuleParameters(toPrettyJson(payload.rule_parameters || {}));
      }
    } catch {
      setError('Settings service unavailable. Using local configuration snapshot.');
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  const parseJson = (value: string, label: string) => {
    try {
      return JSON.parse(value);
    } catch {
      throw new Error(`${label} contains invalid JSON.`);
    }
  };

  const saveCredit = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const response = await fetch(`${API}/credit/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          active_adapter: creditAdapter,
          risk_thresholds: parseJson(creditRiskThresholds, 'Credit risk thresholds'),
          rule_parameters: parseJson(creditRuleParameters, 'Credit rule parameters')
        })
      });
      if (!response.ok) throw new Error('Credit settings save failed.');
      setMessage('Credit engine configuration saved.');
    } catch (exc: any) {
      setError(exc.message || 'Credit settings save failed.');
    } finally {
      setLoading(false);
    }
  };

  const saveFhc = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const response = await fetch(`${API}/fhc/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          weights: parseJson(fhcWeights, 'FHC weights'),
          thresholds: parseJson(fhcThresholds, 'FHC thresholds')
        })
      });
      if (!response.ok) throw new Error('FHC settings save failed.');
      setMessage('Financial Health Card configuration saved.');
    } catch (exc: any) {
      setError(exc.message || 'FHC settings save failed.');
    } finally {
      setLoading(false);
    }
  };

  const saveFraud = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const response = await fetch(`${API}/rbi/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          active_adapter: fraudAdapter,
          rule_parameters: parseJson(fraudRuleParameters, 'Fraud rule parameters')
        })
      });
      if (!response.ok) throw new Error('Fraud settings save failed.');
      setMessage('RBI fraud configuration saved.');
    } catch (exc: any) {
      setError(exc.message || 'Fraud settings save failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 1 }}>
      <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" spacing={2} sx={{ mb: 3 }}>
        <Box>
          <Typography variant="h5" fontWeight="bold">Settings</Typography>
          <Typography variant="body2" color="text.secondary">
            Configure the credit, financial health, and fraud control planes.
          </Typography>
        </Box>
        <Button variant="outlined" startIcon={<Refresh />} onClick={loadSettings} disabled={loading}>Reload Settings</Button>
      </Stack>

      {loading && <LinearProgress sx={{ mb: 2 }} />}
      {message && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage(null)}>{message}</Alert>}
      {error && <Alert severity="warning" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Tabs value={tab} onChange={(_, value) => setTab(value)} sx={{ mb: 3 }}>
          <Tab label="Credit Engine" />
          <Tab label="Financial Health Card" />
          <Tab label="Fraud Registry" />
        </Tabs>

        {tab === 0 && (
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <TextField select fullWidth label="Active Adapter" value={creditAdapter} onChange={(e) => setCreditAdapter(e.target.value)}>
                {ADAPTER_OPTIONS.map((option) => <MenuItem key={option} value={option}>{option}</MenuItem>)}
              </TextField>
            </Grid>
            <Grid item xs={12} md={8}>
              <TextField fullWidth multiline minRows={6} label="Rule Parameters JSON" value={creditRuleParameters} onChange={(e) => setCreditRuleParameters(e.target.value)} />
            </Grid>
            <Grid item xs={12} md={8}>
              <TextField fullWidth multiline minRows={5} label="Risk Thresholds JSON" value={creditRiskThresholds} onChange={(e) => setCreditRiskThresholds(e.target.value)} />
            </Grid>
            <Grid item xs={12}>
              <Button variant="contained" startIcon={<Save />} onClick={saveCredit} disabled={loading}>Save Credit Settings</Button>
            </Grid>
          </Grid>
        )}

        {tab === 1 && (
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField fullWidth multiline minRows={6} label="Weights JSON" value={fhcWeights} onChange={(e) => setFhcWeights(e.target.value)} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField fullWidth multiline minRows={6} label="Thresholds JSON" value={fhcThresholds} onChange={(e) => setFhcThresholds(e.target.value)} />
            </Grid>
            <Grid item xs={12}>
              <Button variant="contained" startIcon={<Save />} onClick={saveFhc} disabled={loading}>Save FHC Settings</Button>
            </Grid>
          </Grid>
        )}

        {tab === 2 && (
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <TextField select fullWidth label="Active Adapter" value={fraudAdapter} onChange={(e) => setFraudAdapter(e.target.value)}>
                {ADAPTER_OPTIONS.map((option) => <MenuItem key={option} value={option}>{option}</MenuItem>)}
              </TextField>
            </Grid>
            <Grid item xs={12} md={8}>
              <TextField fullWidth multiline minRows={6} label="Rule Parameters JSON" value={fraudRuleParameters} onChange={(e) => setFraudRuleParameters(e.target.value)} />
            </Grid>
            <Grid item xs={12}>
              <Button variant="contained" startIcon={<Save />} onClick={saveFraud} disabled={loading}>Save Fraud Settings</Button>
            </Grid>
          </Grid>
        )}
      </Paper>

      <Divider sx={{ my: 3 }} />
      <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 1 }}>Validation</Typography>
        <Typography variant="body2" color="text.secondary">
          This page loads the live service configs, accepts edits, validates JSON before save, and writes the active settings back to the backend.
        </Typography>
      </Paper>
    </Box>
  );
};

export default SettingsPage;