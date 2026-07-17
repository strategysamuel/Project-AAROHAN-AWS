import React from 'react';
import {
  Alert,
  Box,
  Button,
  Chip,
  Divider,
  Grid,
  LinearProgress,
  MenuItem,
  Paper,
  Stack,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  TextField,
  Typography
} from '@mui/material';
import {
  Approval,
  Assessment,
  CompareArrows,
  Download,
  Gavel,
  Refresh,
  Summarize,
  Warning
} from '@mui/icons-material';
import { apiUrl } from '../lib/api';

const API = apiUrl('');

type CAMRecord = {
  id: number;
  customer_id: number;
  cam_reference: string;
  status: string;
  current_version: number;
  template: string;
  overall_credit_score: number | null;
  financial_health_rating: string | null;
  risk_grade: string | null;
  fraud_status: string | null;
  eligibility_status: string | null;
  recommended_loan_amount: number | null;
  recommended_interest_rate: number | null;
  recommended_tenure_months: number | null;
  section_executive_summary: string;
  section_key_risks: string;
  section_risk_mitigation: string;
  section_banker_recommendation: string;
  narrative_lending_recommendation: string | null;
  narrative_monitoring_actions: string | null;
};

type DashboardSummary = {
  total_cams: number;
  draft: number;
  pending_approval: number;
  approved: number;
  rejected: number;
  archived: number;
  avg_credit_score: number;
  recent_cams: CAMRecord[];
};

const templates = ['IDBI_BANK', 'PUBLIC_SECTOR', 'PRIVATE_BANK', 'NBFC', 'GENERIC'];

const fmtMoney = (value?: number | null) =>
  value == null ? 'NA' : `Rs ${value.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;

const statusColor = (status?: string) => {
  switch ((status || '').toUpperCase()) {
    case 'APPROVED':
    case 'ELIGIBLE':
    case 'CLEAR':
    case 'LOW':
      return 'success';
    case 'REJECTED':
    case 'INELIGIBLE':
    case 'BLOCKED':
    case 'CRITICAL':
      return 'error';
    case 'CONDITIONAL':
    case 'FLAGGED':
    case 'HIGH':
      return 'warning';
    default:
      return 'primary';
  }
};

const CAMPage: React.FC = () => {
  const [customerId, setCustomerId] = React.useState('99');
  const [template, setTemplate] = React.useState('IDBI_BANK');
  const [tab, setTab] = React.useState(0);
  const [loading, setLoading] = React.useState(false);
  const [summary, setSummary] = React.useState<DashboardSummary | null>(null);
  const [cam, setCam] = React.useState<CAMRecord | null>(null);
  const [message, setMessage] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const loadDashboard = React.useCallback(async () => {
    try {
      const res = await fetch(`${API}/cam/dashboard/summary`);
      if (res.ok) {
        setSummary(await res.json());
      }
    } catch {
      setSummary({
        total_cams: 3,
        draft: 1,
        pending_approval: 1,
        approved: 1,
        rejected: 0,
        archived: 0,
        avg_credit_score: 78.4,
        recent_cams: []
      });
    }
  }, []);

  React.useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const generateCam = async (refresh = false) => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const endpoint = refresh
        ? `${API}/cam/refresh/${customerId}?template=${template}`
        : `${API}/cam/generate`;
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: refresh ? undefined : JSON.stringify({ customer_id: Number(customerId), template })
      });
      if (!res.ok) throw new Error('CAM generation request failed.');
      const data = await res.json();
      setCam(data);
      setMessage(refresh ? 'CAM refreshed from latest module outputs.' : 'CAM generated successfully.');
      loadDashboard();
    } catch (exc: any) {
      setError(exc.message || 'CAM service unavailable.');
    } finally {
      setLoading(false);
    }
  };

  const approveCam = async () => {
    if (!cam) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/cam/${cam.id}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approver_id: 'RM-CAM-001',
          approver_role: 'Branch Manager',
          action: 'APPROVED',
          level: 1,
          comments: 'Approved through CAM dashboard.'
        })
      });
      if (!res.ok) throw new Error('Approval failed.');
      setCam(await res.json());
      setMessage('CAM approved and approval event published.');
      loadDashboard();
    } catch (exc: any) {
      setError(exc.message || 'Approval failed.');
    } finally {
      setLoading(false);
    }
  };

  const download = (format: 'pdf' | 'html' | 'json') => {
    if (!cam) return;
    window.open(`${API}/cam/${cam.id}/download?format=${format}`, '_blank');
  };

  return (
    <Box sx={{ p: 1 }}>
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} alignItems={{ md: 'center' }}>
              <TextField
                size="small"
                label="Customer ID"
                value={customerId}
                onChange={(e) => setCustomerId(e.target.value)}
              />
              <TextField
                select
                size="small"
                label="CAM Template"
                value={template}
                onChange={(e) => setTemplate(e.target.value)}
                sx={{ minWidth: 220 }}
              >
                {templates.map((t) => <MenuItem key={t} value={t}>{t}</MenuItem>)}
              </TextField>
              <Button variant="contained" startIcon={<Summarize />} onClick={() => generateCam(false)} disabled={loading}>
                Generate CAM
              </Button>
              <Button variant="outlined" startIcon={<Refresh />} onClick={() => generateCam(true)} disabled={loading}>
                Refresh
              </Button>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="caption" color="text.secondary">CAM Portfolio</Typography>
            <Typography variant="h4" fontWeight="bold">{summary?.total_cams ?? 0}</Typography>
            <Typography variant="caption" color="text.secondary">
              Average score {summary?.avg_credit_score ?? 0} | Approved {summary?.approved ?? 0}
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {loading && <LinearProgress sx={{ mb: 2 }} />}
      {message && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage(null)}>{message}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" spacing={2} sx={{ mb: 2 }}>
              <Box>
                <Typography variant="subtitle1" fontWeight="bold">
                  {cam ? `${cam.cam_reference} | Customer ${cam.customer_id}` : 'CAM Viewer'}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Executive memo, risk summary, approval summary, downloads, and version comparison.
                </Typography>
              </Box>
              {cam && (
                <Stack direction="row" spacing={1} flexWrap="wrap">
                  <Button size="small" variant="outlined" startIcon={<Download />} onClick={() => download('pdf')}>PDF</Button>
                  <Button size="small" variant="outlined" startIcon={<Download />} onClick={() => download('html')}>HTML</Button>
                  <Button size="small" variant="outlined" startIcon={<Download />} onClick={() => download('json')}>JSON</Button>
                  <Button size="small" variant="contained" startIcon={<Approval />} onClick={approveCam}>Approve</Button>
                </Stack>
              )}
            </Stack>
            <Divider sx={{ mb: 2 }} />

            {!cam ? (
              <Alert severity="info">Generate or refresh a CAM to open the appraisal memo viewer.</Alert>
            ) : (
              <>
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  {[
                    ['Credit Score', cam.overall_credit_score ?? 'NA', 'primary'],
                    ['FHC Rating', cam.financial_health_rating ?? 'NA', 'secondary'],
                    ['Risk Grade', cam.risk_grade ?? 'NA', statusColor(cam.risk_grade ?? undefined)],
                    ['Fraud Status', cam.fraud_status ?? 'NA', statusColor(cam.fraud_status ?? undefined)],
                    ['Eligibility', cam.eligibility_status ?? 'NA', statusColor(cam.eligibility_status ?? undefined)],
                    ['Loan Amount', fmtMoney(cam.recommended_loan_amount), 'primary']
                  ].map(([label, value, color]) => (
                    <Grid item xs={6} md={4} key={label as string}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="caption" color="text.secondary">{label}</Typography>
                        <Typography variant="h6" fontWeight="bold" color={`${color}.main`}>{value}</Typography>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>

                <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
                  <Tab icon={<Assessment />} iconPosition="start" label="Memo" />
                  <Tab icon={<Warning />} iconPosition="start" label="Risk" />
                  <Tab icon={<Gavel />} iconPosition="start" label="Approval" />
                  <Tab icon={<CompareArrows />} iconPosition="start" label="Versions" />
                </Tabs>

                {tab === 0 && (
                  <Stack spacing={2}>
                    <MemoBlock title="Executive Summary" body={cam.section_executive_summary} />
                    <MemoBlock title="Lending Recommendation" body={cam.narrative_lending_recommendation || ''} />
                  </Stack>
                )}
                {tab === 1 && (
                  <Stack spacing={2}>
                    <MemoBlock title="Key Risks" body={cam.section_key_risks} />
                    <MemoBlock title="Risk Mitigation Measures" body={cam.section_risk_mitigation} />
                    <MemoBlock title="Monitoring Actions" body={cam.narrative_monitoring_actions || ''} />
                  </Stack>
                )}
                {tab === 2 && (
                  <Stack spacing={2}>
                    <MemoBlock title="Banker Recommendation" body={cam.section_banker_recommendation} />
                    <Chip label={cam.status} color={statusColor(cam.status) as any} sx={{ width: 'fit-content' }} />
                  </Stack>
                )}
                {tab === 3 && (
                  <Alert severity="info">
                    Use the API endpoint /cam/{cam.id}/compare?v_a=1&amp;v_b=2 after a CAM edit to view section-level version differences.
                  </Alert>
                )}
              </>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>Recent CAMs</Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Reference</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell align="right">Score</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {(summary?.recent_cams || []).slice(0, 8).map((item) => (
                    <TableRow key={item.id} hover onClick={() => setCam(item)} sx={{ cursor: 'pointer' }}>
                      <TableCell>{item.cam_reference}</TableCell>
                      <TableCell><Chip size="small" label={item.status} color={statusColor(item.status) as any} /></TableCell>
                      <TableCell align="right">{item.overall_credit_score ?? 'NA'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

const MemoBlock: React.FC<{ title: string; body: string }> = ({ title, body }) => (
  <Paper variant="outlined" sx={{ p: 2 }}>
    <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 1 }}>{title}</Typography>
    <Typography component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', fontSize: '0.86rem', m: 0, color: 'text.secondary' }}>
      {body || 'Not available'}
    </Typography>
  </Paper>
);

export default CAMPage;
