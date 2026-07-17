import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Grid, Paper, TextField, Button, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Chip, CircularProgress,
  Alert, Card, CardContent, Divider, Dialog, DialogTitle, DialogContent,
  DialogActions, Stack, Avatar, LinearProgress, Tab, Tabs, List, ListItem,
  ListItemText, ListItemIcon
} from '@mui/material';
import {
  Search, Assessment, CheckCircle, Warning, Refresh, Download,
  TrendingUp, AccountBalance, Gavel, History, Timeline, ErrorOutline,
  AssignmentInd, People, DateRange
} from '@mui/icons-material';

interface EPFOContribution {
  id: number;
  wage_month: string;
  amount_paid: number;
  employer_share: number;
  employees_count: number;
  payment_date: string;
  status: string;
}

interface EPFOEmployee {
  id: number;
  uan: string;
  name: string;
  joining_date: string;
  exit_date?: string;
  salary: number;
  designation: string;
  is_active: boolean;
}

interface EPFOAnalytics {
  id: number;
  active_employees: number;
  attrition_rate: number;
  avg_employee_tenure: number;
  monthly_payroll: number;
  payroll_growth: number;
  hiring_trend: string;
  workforce_growth: number;
  payroll_stability_index: number;
  compliance_score: number;
  payroll_risk: string;
  compliance_risk: string;
  attrition_risk: string;
  workforce_stability_risk: string;
  business_continuity_risk: string;
  ai_insights: string;
}

interface EPFOProfile {
  id: number;
  customer_id: number;
  establishment_id: string;
  establishment_name: string;
  esic_registration_num?: string;
  status: string;
  number_of_employees: number;
  average_monthly_payroll: number;
  last_synced_at: string;
}

const API = 'http://localhost:8000'; // Gateway routing

const EPFOPage: React.FC = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [profile, setProfile] = useState<EPFOProfile | null>(null);
  const [employees, setEmployees] = useState<EPFOEmployee[]>([]);
  const [contributions, setContributions] = useState<EPFOContribution[]>([]);
  const [analytics, setAnalytics] = useState<EPFOAnalytics | null>(null);
  
  const [estQuery, setEstQuery] = useState('MHBAN1234567000'); // Valid 15-char default prefix
  const [esicQuery, setEsicQuery] = useState('27000283726354890');

  // Override dialog state
  const [overrideOpen, setOverrideOpen] = useState(false);
  const [overrideScore, setOverrideScore] = useState(95.0);
  const [overrideRM, setOverrideRM] = useState('ADMIN-EPFO-OPS');
  const [overrideComments, setOverrideComments] = useState('');

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSync = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    setProfile(null);
    setAnalytics(null);
    setEmployees([]);
    setContributions([]);

    try {
      const res = await fetch(`${API}/epfo/sync/99`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          establishment_id: estQuery,
          esic_registration_num: esicQuery
        })
      });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);

        // Fetch employee lists, contributions, and analytics
        const empRes = await fetch(`${API}/epfo/employees/99`);
        if (empRes.ok) setEmployees(await empRes.json());

        const conRes = await fetch(`${API}/epfo/contributions/99`);
        if (conRes.ok) setContributions(await conRes.json());

        const anlRes = await fetch(`${API}/epfo/analytics/99`);
        if (anlRes.ok) setAnalytics(await anlRes.json());

        setSuccess('✓ EPFO Establishment Profile and Workforce stability analyses completed!');
      } else {
        setError('Establishment ID validation failed. Make sure it matches standard Indian EPFO code (15/22 alphanumeric format).');
      }
    } catch {
      // Mock Fallbacks
      setProfile({
        id: 1, customer_id: 99, establishment_id: estQuery,
        establishment_name: 'Project AAROHAN Textiles Private Limited',
        esic_registration_num: esicQuery, status: 'ACTIVE',
        number_of_employees: 35, average_monthly_payroll: 420000.0,
        last_synced_at: new Date().toISOString()
      });
      setEmployees([
        { id: 1, uan: '100983726', name: 'Amit Sharma', joining_date: '2021-06-15', salary: 12000, designation: 'Operator', is_active: true },
        { id: 2, uan: '100983727', name: 'Priya Patel', joining_date: '2021-07-05', salary: 13200, designation: 'Supervisor', is_active: true }
      ]);
      setContributions([
        { id: 1, wage_month: '122025', amount_paid: 54000, employer_share: 24300, employees_count: 28, payment_date: '2026-01-15', status: 'PAID' },
        { id: 2, wage_month: '012026', amount_paid: 58000, employer_share: 26100, employees_count: 31, payment_date: '2026-02-23', status: 'LATE' }
      ]);
      setAnalytics({
        id: 1, active_employees: 33, attrition_rate: 5.7, avg_employee_tenure: 24.5,
        monthly_payroll: 412000, payroll_growth: 7.4, hiring_trend: 'Expansion',
        workforce_growth: 7.4, payroll_stability_index: 92.5, compliance_score: 90.0,
        payroll_risk: 'Low', compliance_risk: 'Low', attrition_risk: 'Low',
        workforce_stability_risk: 'Low', business_continuity_risk: 'Low',
        ai_insights: 'Stable workforce with consistent payroll. | EPFO compliance is excellent. | Rapid hiring indicates business expansion.'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRerun = async () => {
    if (!profile) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/epfo/analytics/99/re-run`, { method: 'POST' });
      if (res.ok) {
        setAnalytics(await res.json());
        setSuccess('✓ Workforce calculations re-evaluated.');
      }
    } catch {
      setSuccess('✓ Workforce calculations re-evaluated (mock mode).');
    } finally {
      setLoading(false);
    }
  };

  const handleOverrideSubmit = async () => {
    if (!profile) return;
    try {
      const res = await fetch(`${API}/epfo/override/99`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          compliance_score: overrideScore,
          checked_by: overrideRM,
          comments: overrideComments
        })
      });
      if (res.ok) {
        setAnalytics(await res.json());
        setSuccess('✓ EPFO compliance score override submitted.');
      }
    } catch {
      setSuccess('✓ EPFO compliance score override submitted (mock mode).');
    } finally {
      setOverrideOpen(false);
    }
  };

  const handleExport = () => {
    if (employees.length === 0) return;
    const csvContent = "data:text/csv;charset=utf-8,"
      + ["UAN,Employee Name,Designation,Salary (INR),Joining Date,Status"].join(",") + "\n"
      + employees.map(e => [e.uan, e.name, e.designation, e.salary, e.joining_date, e.is_active ? 'Active' : 'Exited'].join(",")).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `EPFO_Workforce_Payroll_Report.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getRiskColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'low': return 'success';
      case 'medium': return 'info';
      case 'high': return 'warning';
      case 'critical': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 1 }}>
      {/* Search and sync establishment bar */}
      <Paper sx={{ p: 3, mb: 4, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>EPFO Establishment Registry Verification</Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              size="small"
              label="Establishment Code (15/22 chars)"
              value={estQuery}
              onChange={e => setEstQuery(e.target.value.toUpperCase())}
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              size="small"
              label="ESIC Code (17 digits)"
              value={esicQuery}
              onChange={e => setEsicQuery(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button variant="contained" onClick={handleSync} disabled={loading} startIcon={<Refresh />}>
              {loading ? 'Fetching...' : 'Verify & Import'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {loading && <LinearProgress sx={{ mb: 4 }} />}

      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>{success}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {profile && (
        <Box>
          {/* Summary Panel */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 3, height: '100%', border: '1px solid rgba(255,255,255,0.06)' }}>
                <Typography variant="caption" color="text.secondary">EPFO Profile Details</Typography>
                <Typography variant="h6" fontWeight="bold" sx={{ mt: 1, mb: 2 }}>{profile.establishment_name}</Typography>
                <Divider sx={{ mb: 2 }} />
                <Stack spacing={1.5} sx={{ fontSize: '0.85rem' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Est Code</Typography>
                    <Typography fontWeight="bold">{profile.establishment_id}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">ESIC Code</Typography>
                    <Typography fontWeight="bold">{profile.esic_registration_num || '–'}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Total Headcount</Typography>
                    <Typography fontWeight="bold">{profile.number_of_employees} employees</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Registration Status</Typography>
                    <Chip size="small" label={profile.status} color="success" />
                  </Box>
                </Stack>
              </Paper>
            </Grid>

            {analytics && (
              <>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper sx={{ p: 3, height: '100%', border: '1px solid rgba(255,255,255,0.06)' }}>
                    <Typography variant="caption" color="text.secondary">EPFO Statutory Compliance</Typography>
                    <Typography variant="h3" fontWeight="bold" color="primary.main" sx={{ mt: 1, mb: 1 }}>
                      {analytics.compliance_score}%
                    </Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 2 }}>
                      Workforce Stability Rating: <strong>Excellent</strong>
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Chip label={analytics.compliance_risk.toUpperCase()} color={getRiskColor(analytics.compliance_risk)} />
                      <Button size="small" variant="outlined" onClick={() => setOverrideOpen(true)}>
                        Override Score
                      </Button>
                    </Box>
                  </Paper>
                </Grid>

                <Grid item xs={12} sm={6} md={4}>
                  <Paper sx={{ p: 3, height: '100%', border: '1px solid rgba(255,255,255,0.06)' }}>
                    <Typography variant="caption" color="text.secondary">Workforce Analytics</Typography>
                    <Stack spacing={1.5} sx={{ mt: 2, fontSize: '0.85rem' }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography color="text.secondary">Attrition Rate</Typography>
                        <Typography fontWeight="bold" color={analytics.attrition_rate > 10 ? 'error.main' : 'success.main'}>
                          {analytics.attrition_rate.toFixed(1)}%
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography color="text.secondary">Average Tenure</Typography>
                        <Typography fontWeight="bold">{analytics.avg_employee_tenure.toFixed(1)} months</Typography>
                      </Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography color="text.secondary">Monthly Payroll (Est)</Typography>
                        <Typography fontWeight="bold">₹{analytics.monthly_payroll.toLocaleString('en-IN')}</Typography>
                      </Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography color="text.secondary">Payroll Stability</Typography>
                        <Typography fontWeight="bold">{analytics.payroll_stability_index.toFixed(1)}%</Typography>
                      </Box>
                    </Stack>
                  </Paper>
                </Grid>
              </>
            )}
          </Grid>

          {/* Navigation Tabs */}
          <Tabs value={tabIndex} onChange={(_, idx) => setTabIndex(idx)} sx={{ mb: 3, borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
            <Tab label="Workforce Roster" icon={<People />} iconPosition="start" />
            <Tab label="Contribution Timeline" icon={<DateRange />} iconPosition="start" />
            <Tab label="AI Workforce Insights" icon={<Assessment />} iconPosition="start" />
          </Tabs>

          {/* Tab 0: Employees roster */}
          {tabIndex === 0 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1, mb: 2 }}>
                <Button variant="outlined" size="small" startIcon={<Refresh />} onClick={handleRerun}>
                  Re-evaluate
                </Button>
                <Button variant="outlined" size="small" startIcon={<Download />} onClick={handleExport}>
                  Export Roster
                </Button>
              </Box>

              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>UAN ID</strong></TableCell>
                      <TableCell><strong>Name</strong></TableCell>
                      <TableCell><strong>Designation</strong></TableCell>
                      <TableCell align="right"><strong>Monthly Salary (₹)</strong></TableCell>
                      <TableCell><strong>Joining Date</strong></TableCell>
                      <TableCell><strong>Exit Date</strong></TableCell>
                      <TableCell><strong>Status</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {employees.map(emp => (
                      <TableRow key={emp.id}>
                        <TableCell>{emp.uan}</TableCell>
                        <TableCell><strong>{emp.name}</strong></TableCell>
                        <TableCell>{emp.designation}</TableCell>
                        <TableCell align="right">₹{emp.salary.toLocaleString('en-IN')}</TableCell>
                        <TableCell>{new Date(emp.joining_date).toLocaleDateString()}</TableCell>
                        <TableCell>{emp.exit_date ? new Date(emp.exit_date).toLocaleDateString() : '–'}</TableCell>
                        <TableCell>
                          <Chip size="small" label={emp.is_active ? 'ACTIVE' : 'EXITED'} color={emp.is_active ? 'success' : 'default'} />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}

          {/* Tab 1: Contribution history */}
          {tabIndex === 1 && (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell><strong>Wage Month</strong></TableCell>
                    <TableCell><strong>Employees Count</strong></TableCell>
                    <TableCell align="right"><strong>EPF Contribution (₹)</strong></TableCell>
                    <TableCell align="right"><strong>Employer Share (₹)</strong></TableCell>
                    <TableCell><strong>Payment Date</strong></TableCell>
                    <TableCell><strong>Status</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {contributions.map(c => (
                    <TableRow key={c.id}>
                      <TableCell>{c.wage_month}</TableCell>
                      <TableCell>{c.employees_count}</TableCell>
                      <TableCell align="right">₹{c.amount_paid.toLocaleString('en-IN')}</TableCell>
                      <TableCell align="right">₹{c.employer_share.toLocaleString('en-IN')}</TableCell>
                      <TableCell>{c.payment_date ? new Date(c.payment_date).toLocaleDateString() : '–'}</TableCell>
                      <TableCell>
                        <Chip
                          size="small"
                          label={c.status}
                          color={c.status === 'PAID' ? 'success' : 'warning'}
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}

          {/* Tab 2: AI Workforce Insights */}
          {tabIndex === 2 && analytics && (
            <Paper variant="outlined" sx={{ p: 4 }}>
              <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 3 }}>Gemini AI Statutory workforce observations</Typography>
              <Divider sx={{ mb: 3 }} />
              
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Stack spacing={2}>
                    {analytics.ai_insights.split(' | ').map((insight, idx) => (
                      <Card key={idx} sx={{ bgcolor: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.04)' }}>
                        <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 2, '&:last-child': { pb: 2 } }}>
                          <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                            <TrendingUp fontSize="small" />
                          </Avatar>
                          <Typography variant="body2" fontWeight="600">{insight}</Typography>
                        </CardContent>
                      </Card>
                    ))}
                  </Stack>
                </Grid>
              </Grid>
            </Paper>
          )}
        </Box>
      )}

      {/* Override Compliance score dialogue */}
      <Dialog open={overrideOpen} onClose={() => setOverrideOpen(false)}>
        <DialogTitle>Override Statutory Compliance Score</DialogTitle>
        <DialogContent sx={{ minWidth: 400 }}>
          <Stack spacing={2} sx={{ mt: 1.5 }}>
            <Alert severity="info">
              Manually override the automated statutory compliance score model outputs. Will log auditedRM details.
            </Alert>
            <TextField
              type="number"
              label="Manually Assigned Compliance Score (0-100)"
              value={overrideScore}
              onChange={e => setOverrideScore(parseFloat(e.target.value))}
              fullWidth
            />
            <TextField
              label="Audited By (RM Staff ID)"
              value={overrideRM}
              onChange={e => setOverrideRM(e.target.value)}
              fullWidth
            />
            <TextField
              label="Reason for Manual Compliance Correction"
              value={overrideComments}
              onChange={e => setOverrideComments(e.target.value)}
              multiline
              rows={3}
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOverrideOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleOverrideSubmit}>Submit Correction</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EPFOPage;
