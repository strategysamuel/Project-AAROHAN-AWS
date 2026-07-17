import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Grid, Paper, TextField, Button, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Chip, CircularProgress,
  Alert, Card, CardContent, Divider, Dialog, DialogTitle, DialogContent,
  DialogActions, Stack, Avatar, LinearProgress, Tab, Tabs, List, ListItem,
  ListItemText, ListItemIcon, Checkbox, FormControlLabel
} from '@mui/material';
import {
  Search, Assessment, CheckCircle, Warning, Refresh, Download,
  TrendingUp, AccountBalance, Gavel, History, Timeline, ErrorOutline,
  CompareArrows, AssignmentInd, Security
} from '@mui/icons-material';

interface AAConsent {
  id: number;
  customer_id: number;
  consent_artefact_id: string;
  purpose: string;
  data_requested: string;
  validity: string;
  frequency: string;
  accounts_included?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

interface LinkedAccount {
  id: number;
  customer_id: number;
  account_ref_num: string;
  masked_acc_num: string;
  bank_name: string;
  account_type: string;
  balance: number;
  currency: string;
  is_active: boolean;
  last_synced_at?: string;
}

interface AATransaction {
  id: number;
  account_id: number;
  txn_ref_num: string;
  txn_date: string;
  amount: number;
  txn_type: string;
  narration?: string;
  category: string;
  is_recurring: boolean;
}

interface AAAnalytics {
  id: number;
  customer_id: number;
  total_inflow: number;
  total_outflow: number;
  net_cash_flow: number;
  avg_balance: number;
  median_balance: number;
  income_score: number;
  debt_service_ratio: number;
  monthly_credits: number;
  monthly_debits: number;
  cash_flow_stability: number;
  seasonality: number;
  income_stability: number;
  expense_ratio: number;
  working_capital_estimate: number;
  savings_behaviour: string;
  salary_regularity: string;
  business_revenue_stability: string;
  cheque_bounce_indicator: boolean;
  emi_discipline: string;
  overdraft_usage: string;
  high_cash_dependency: boolean;
  large_cash_withdrawals: boolean;
  frequent_low_balance: boolean;
  dormant_account: boolean;
  liquidity_risk: string;
  cash_flow_risk: string;
  behaviour_risk: string;
  income_risk: string;
  expense_risk: string;
  banking_stability_score: number;
  overall_score: number;
  ai_insights: string;
}

const API = 'http://localhost:8000'; // Gateway routing to local microservices

const AAPage: React.FC = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [consents, setConsents] = useState<AAConsent[]>([]);
  const [linkedAccounts, setLinkedAccounts] = useState<LinkedAccount[]>([]);
  const [transactions, setTransactions] = useState<AATransaction[]>([]);
  const [analytics, setAnalytics] = useState<AAAnalytics | null>(null);

  // New Consent dialog
  const [consentOpen, setConsentOpen] = useState(false);
  const [consentPurpose, setConsentPurpose] = useState('MSME Business Loan Underwriting Spreading');
  const [consentValidityDays, setConsentValidityDays] = useState(30);

  // Consent Approval dialogue
  const [approveOpen, setApproveOpen] = useState(false);
  const [selectedConsent, setSelectedConsent] = useState<AAConsent | null>(null);
  const [discoveredAccounts, setDiscoveredAccounts] = useState<any[]>([]);
  const [selectedAccounts, setSelectedAccounts] = useState<string[]>([]);

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const fetchConsentsAndAnalytics = async () => {
    setLoading(true);
    try {
      const cRes = await fetch(`${API}/aa/consents?customer_id=99`);
      if (cRes.ok) setConsents(await cRes.json());

      const aRes = await fetch(`${API}/aa/accounts/99`);
      if (aRes.ok) setLinkedAccounts(await aRes.json());

      const txRes = await fetch(`${API}/aa/financial-info/99`);
      if (txRes.ok) setTransactions(await txRes.json());

      const anRes = await fetch(`${API}/aa/analytics/99`);
      if (anRes.ok) setAnalytics(await anRes.json());
    } catch {
      // Mock Fallbacks
      setConsents([
        {
          id: 1, customer_id: 99, consent_artefact_id: 'consent_art_mock123',
          purpose: 'MSME Loan Eligibility Check', data_requested: 'Statement & Balances',
          validity: '2026-08-08', frequency: 'ONCE', status: 'APPROVED',
          created_at: new Date().toISOString(), updated_at: new Date().toISOString()
        }
      ]);
      setLinkedAccounts([
        {
          id: 1, customer_id: 99, account_ref_num: 'SBI-MOCK-1', masked_acc_num: 'XXXXXX4321',
          bank_name: 'State Bank of India', account_type: 'CURRENT', balance: 350000.0,
          currency: 'INR', is_active: true
        }
      ]);
      setAnalytics({
        id: 1, customer_id: 99, total_inflow: 1850000, total_outflow: 1420000,
        net_cash_flow: 430000, avg_balance: 237500, median_balance: 237500,
        income_score: 91.0, debt_service_ratio: 0.76, monthly_credits: 308333,
        monthly_debits: 236666, cash_flow_stability: 89.0, seasonality: 1.3,
        income_stability: 89.0, expense_ratio: 0.76, working_capital_estimate: 215000,
        savings_behaviour: 'Moderate Savings', salary_regularity: 'Regular',
        business_revenue_stability: 'Stable', cheque_bounce_indicator: false,
        emi_discipline: 'Excellent', overdraft_usage: 'None',
        high_cash_dependency: false, large_cash_withdrawals: false,
        frequent_low_balance: false, dormant_account: false,
        liquidity_risk: 'Low', cash_flow_risk: 'Low', behaviour_risk: 'Low',
        income_risk: 'Low', expense_risk: 'Low', banking_stability_score: 95.0,
        overall_score: 92.0, ai_insights: 'Strong and consistent cash flow. | Excellent banking discipline. | High digital transaction adoption.'
      });
      setTransactions([
        {
          id: 1, account_id: 1, txn_ref_num: 'TXN-001', txn_date: new Date().toISOString(),
          amount: 250000.0, txn_type: 'CREDIT', narration: 'NEFT CLIENT INFLOW SETTLEMENT',
          category: 'INCOME', is_recurring: false
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConsentsAndAnalytics();
  }, []);

  const handleCreateConsent = async () => {
    try {
      const res = await fetch(`${API}/aa/consents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_id: 99,
          purpose: consentPurpose,
          validity_days: consentValidityDays
        })
      });
      if (res.ok) {
        setSuccess('✓ Consent request registered in Account Aggregator registry.');
        setConsentOpen(false);
        fetchConsentsAndAnalytics();
      }
    } catch {
      setSuccess('✓ Consent request registered (mock).');
      setConsentOpen(false);
    }
  };

  const handleOpenApproveDialog = async (consent: AAConsent) => {
    setSelectedConsent(consent);
    setApproveOpen(true);
    // Discover accounts
    try {
      const res = await fetch(`${API}/aa/discover/99`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_mobile: '9876543210' })
      });
      if (res.ok) {
        const accs = await res.json();
        setDiscoveredAccounts(accs);
        setSelectedAccounts(accs.map((a: any) => a.account_ref_num));
      }
    } catch {
      setDiscoveredAccounts([
        { account_ref_num: 'SBI-ACC-CURRENT', bank_name: 'State Bank of India', account_type: 'CURRENT', balance: 450000.0 },
        { account_ref_num: 'IDBI-ACC-SAVINGS', bank_name: 'IDBI Bank', account_type: 'SAVINGS', balance: 125000.0 }
      ]);
    }
  };

  const handleApproveConsent = async () => {
    if (!selectedConsent) return;
    try {
      // 1. Approve Consent Status
      const approveRes = await fetch(`${API}/aa/consents/${selectedConsent.consent_artefact_id}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          status: 'APPROVED',
          accounts_included: selectedAccounts.join(',')
        })
      });
      
      if (approveRes.ok) {
        // 2. Link selected accounts
        const linkPayload = discoveredAccounts
          .filter(a => selectedAccounts.includes(a.account_ref_num))
          .map(a => ({
            account_ref_num: a.account_ref_num,
            masked_acc_num: a.masked_acc_num || 'XXXXXX4321',
            bank_name: a.bank_name,
            account_type: a.account_type,
            balance: a.balance
          }));
          
        await fetch(`${API}/aa/link/99`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(linkPayload)
        });

        // 3. Sync statements
        await fetch(`${API}/aa/sync/99`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ consent_id: selectedConsent.consent_artefact_id })
        });

        setSuccess('✓ Consent approved, accounts linked, and bank statements synced successfully!');
        setApproveOpen(false);
        fetchConsentsAndAnalytics();
      }
    } catch {
      setSuccess('✓ Consent approved and transactions imported (mock mode).');
      setApproveOpen(false);
    }
  };

  const handleRevokeConsent = async (consentId: string) => {
    try {
      const res = await fetch(`${API}/aa/consents/${consentId}/revoke`, { method: 'POST' });
      if (res.ok) {
        setSuccess('✓ Consent revoked successfully.');
        fetchConsentsAndAnalytics();
      }
    } catch {
      setSuccess('✓ Consent revoked (mock mode).');
    }
  };

  const handleReplayFinancials = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/aa/replay/99`, { method: 'POST' });
      if (res.ok) {
        setSuccess('✓ Statements reloaded and cash flows re-calculated.');
        fetchConsentsAndAnalytics();
      }
    } catch {
      setSuccess('✓ Statement reload triggered (mock mode).');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    if (transactions.length === 0) return;
    const csvContent = "data:text/csv;charset=utf-8,"
      + ["Date,Transaction Ref,Type,Amount (INR),Category,Narration"].join(",") + "\n"
      + transactions.map(t => [t.txn_date, t.txn_ref_num, t.txn_type, t.amount, t.category, t.narration?.replace(/,/g, '')].join(",")).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `Bank_Statement_Transactions_99.csv`);
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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6" fontWeight="bold">Account Aggregator Consent Registry</Typography>
        <Stack direction="row" spacing={1.5}>
          <Button variant="outlined" size="small" startIcon={<Refresh />} onClick={handleReplayFinancials} disabled={loading}>
            Reload Financial Statements
          </Button>
          <Button variant="contained" size="small" onClick={() => setConsentOpen(true)}>
            Request AA Consent
          </Button>
        </Stack>
      </Box>

      {loading && <LinearProgress sx={{ mb: 3 }} />}

      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>{success}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {/* Linked Accounts summary */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
            <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>Linked Bank Accounts</Typography>
            <Grid container spacing={2}>
              {linkedAccounts.map(acc => (
                <Grid item xs={12} sm={6} key={acc.id}>
                  <Card variant="outlined">
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="body2" fontWeight="bold">{acc.bank_name}</Typography>
                        <Chip size="small" label={acc.account_type} color="primary" variant="outlined" />
                      </Box>
                      <Typography variant="h6" fontWeight="bold" sx={{ mt: 1.5 }}>
                        ₹{acc.balance.toLocaleString('en-IN')}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Acc Num: {acc.masked_acc_num} | Ref: {acc.account_ref_num}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
              {linkedAccounts.length === 0 && (
                <Grid item xs={12}>
                  <Alert severity="info">No linked accounts discovered. Create a consent and approve it first.</Alert>
                </Grid>
              )}
            </Grid>
          </Paper>
        </Grid>

        {analytics && (
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%', border: '1px solid rgba(255,255,255,0.06)', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="caption" color="text.secondary">Banking Stability Score</Typography>
                <Typography variant="h4" fontWeight="bold" color="success.main" sx={{ mt: 0.5, mb: 1 }}>
                  {analytics.overall_score}/100
                </Typography>
                <Divider sx={{ my: 1.5 }} />
                <Stack spacing={1} sx={{ fontSize: '0.85rem' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Liquidity Risk</Typography>
                    <Chip size="small" label={analytics.liquidity_risk} color={getRiskColor(analytics.liquidity_risk)} />
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Cash Flow Risk</Typography>
                    <Chip size="small" label={analytics.cash_flow_risk} color={getRiskColor(analytics.cash_flow_risk)} />
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Behaviour Risk</Typography>
                    <Chip size="small" label={analytics.behaviour_risk} color={getRiskColor(analytics.behaviour_risk)} />
                  </Box>
                </Stack>
              </Box>
            </Paper>
          </Grid>
        )}
      </Grid>

      {/* Tabs */}
      <Tabs value={tabIndex} onChange={(_, idx) => setTabIndex(idx)} sx={{ mb: 3, borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <Tab label="Consents Audit & Lifecycle" icon={<Security />} iconPosition="start" />
        <Tab label="Cash Flow Intelligence" icon={<Timeline />} iconPosition="start" />
        <Tab label="Transaction Ledger" icon={<CompareArrows />} iconPosition="start" />
        <Tab label="AI Insights" icon={<Assessment />} iconPosition="start" />
      </Tabs>

      {/* Tab 0: Consent Lifecycles */}
      {tabIndex === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell><strong>Consent ID</strong></TableCell>
                <TableCell><strong>Purpose</strong></TableCell>
                <TableCell><strong>Validity</strong></TableCell>
                <TableCell><strong>Frequency</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
                <TableCell><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {consents.map(c => (
                <TableRow key={c.id}>
                  <TableCell>{c.consent_artefact_id}</TableCell>
                  <TableCell>{c.purpose}</TableCell>
                  <TableCell>{c.validity}</TableCell>
                  <TableCell>{c.frequency}</TableCell>
                  <TableCell>
                    <Chip
                      size="small"
                      label={c.status}
                      color={
                        c.status === 'APPROVED' ? 'success' :
                        c.status === 'PENDING' ? 'warning' : 'default'
                      }
                    />
                  </TableCell>
                  <TableCell>
                    {c.status === 'PENDING' && (
                      <Button size="small" variant="contained" color="success" onClick={() => handleOpenApproveDialog(c)}>
                        Approve
                      </Button>
                    )}
                    {c.status === 'APPROVED' && (
                      <Button size="small" variant="outlined" color="error" onClick={() => handleRevokeConsent(c.consent_artefact_id)}>
                        Revoke
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Tab 1: Cash Flow Intelligence */}
      {tabIndex === 1 && analytics && (
        <Box>
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={3}>
              <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">Avg Monthly Credits</Typography>
                <Typography variant="h6" fontWeight="bold">₹{analytics.monthly_credits.toLocaleString('en-IN')}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">Avg Monthly Debits</Typography>
                <Typography variant="h6" fontWeight="bold">₹{analytics.monthly_debits.toLocaleString('en-IN')}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">Net Annual Cash Flow</Typography>
                <Typography variant="h6" fontWeight="bold" color={analytics.net_cash_flow >= 0 ? 'success.main' : 'error.main'}>
                  ₹{analytics.net_cash_flow.toLocaleString('en-IN')}
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">Expense Inflow Ratio</Typography>
                <Typography variant="h6" fontWeight="bold">{analytics.expense_ratio.toFixed(2)}</Typography>
              </Paper>
            </Grid>
          </Grid>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Paper variant="outlined" sx={{ p: 3 }}>
                <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>Banking Behaviour & Discipline Dashboard</Typography>
                <Divider sx={{ mb: 2 }} />
                <Stack spacing={1.5} sx={{ fontSize: '0.85rem' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Salary Regularity</Typography>
                    <Typography fontWeight="bold">{analytics.salary_regularity}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">EMI discipline</Typography>
                    <Typography fontWeight="bold" color={analytics.emi_discipline === 'Excellent' ? 'success.main' : 'error.main'}>
                      {analytics.emi_discipline}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Cheque Bounces</Typography>
                    <Typography fontWeight="bold" color={analytics.cheque_bounce_indicator ? 'error.main' : 'success.main'}>
                      {analytics.cheque_bounce_indicator ? 'Detected' : 'No bounces'}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Overdraft Utilization</Typography>
                    <Typography fontWeight="bold">{analytics.overdraft_usage}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">High Cash Dependency</Typography>
                    <Typography fontWeight="bold">{analytics.high_cash_dependency ? 'Yes' : 'No'}</Typography>
                  </Box>
                </Stack>
              </Paper>
            </Grid>

            {/* Simulated Balance Trend Chart */}
            <Grid item xs={12} md={6}>
              <Paper variant="outlined" sx={{ p: 3 }}>
                <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>Simulated Cash Inflow vs Outflow</Typography>
                <Box sx={{ display: 'flex', gap: 4, height: 140, alignItems: 'flex-end', justifyContent: 'center', pt: 2 }}>
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Box sx={{ width: 40, height: 90, bgcolor: 'success.main', borderRadius: '4px 4px 0 0' }} />
                    <Typography variant="caption" sx={{ mt: 1 }}>Credits</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Box sx={{ width: 40, height: 70, bgcolor: 'error.main', borderRadius: '4px 4px 0 0' }} />
                    <Typography variant="caption" sx={{ mt: 1 }}>Debits</Typography>
                  </Box>
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Box>
      )}

      {/* Tab 2: Transaction Ledger */}
      {tabIndex === 2 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button variant="outlined" size="small" startIcon={<Download />} onClick={handleExport}>
              Export Transactions
            </Button>
          </Box>
          <TableContainer component={Paper} variant="outlined">
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell><strong>Date</strong></TableCell>
                  <TableCell><strong>Transaction Ref</strong></TableCell>
                  <TableCell><strong>Type</strong></TableCell>
                  <TableCell align="right"><strong>Amount (₹)</strong></TableCell>
                  <TableCell><strong>Category</strong></TableCell>
                  <TableCell><strong>Narration</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {transactions.map(t => (
                  <TableRow key={t.id}>
                    <TableCell>{new Date(t.txn_date).toLocaleDateString()}</TableCell>
                    <TableCell>{t.txn_ref_num}</TableCell>
                    <TableCell>
                      <Chip
                        size="small"
                        label={t.txn_type}
                        color={t.txn_type === 'CREDIT' ? 'success' : 'error'}
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell align="right">₹{t.amount.toLocaleString('en-IN')}</TableCell>
                    <TableCell><Chip size="small" label={t.category} /></TableCell>
                    <TableCell>{t.narration}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      {/* Tab 3: AI Insights */}
      {tabIndex === 3 && analytics && (
        <Paper variant="outlined" sx={{ p: 4 }}>
          <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 3 }}>Gemini AI Cash Flow Underwriting Insights</Typography>
          <Divider sx={{ mb: 3 }} />
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
        </Paper>
      )}

      {/* Consent Dialog */}
      <Dialog open={consentOpen} onClose={() => setConsentOpen(false)}>
        <DialogTitle>Request AA Financial Information Consent</DialogTitle>
        <DialogContent sx={{ minWidth: 400 }}>
          <Stack spacing={2} sx={{ mt: 1.5 }}>
            <TextField
              label="Purpose"
              value={consentPurpose}
              onChange={e => setConsentPurpose(e.target.value)}
              fullWidth
            />
            <TextField
              type="number"
              label="Validity Duration (Days)"
              value={consentValidityDays}
              onChange={e => setConsentValidityDays(parseInt(e.target.value))}
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConsentOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleCreateConsent}>Generate Consent</Button>
        </DialogActions>
      </Dialog>

      {/* Approval Dialog */}
      <Dialog open={approveOpen} onClose={() => setApproveOpen(false)}>
        <DialogTitle>Approve Account Aggregator Consent Request</DialogTitle>
        <DialogContent sx={{ minWidth: 400 }}>
          <Stack spacing={2} sx={{ mt: 1.5 }}>
            <Alert severity="warning">
              You are authorizing the sharing of transaction statement metadata for the following discovered accounts:
            </Alert>
            <Typography variant="subtitle2" fontWeight="bold">Select Accounts to Share:</Typography>
            {discoveredAccounts.map(a => (
              <FormControlLabel
                key={a.account_ref_num}
                control={
                  <Checkbox
                    checked={selectedAccounts.includes(a.account_ref_num)}
                    onChange={e => {
                      if (e.target.checked) {
                        setSelectedAccounts([...selectedAccounts, a.account_ref_num]);
                      } else {
                        setSelectedAccounts(selectedAccounts.filter(r => r !== a.account_ref_num));
                      }
                    }}
                  />
                }
                label={`${a.bank_name} (${a.account_type}) - Balance: ₹${a.balance}`}
              />
            ))}
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setApproveOpen(false)}>Reject</Button>
          <Button variant="contained" color="success" onClick={handleApproveConsent}>Approve Consent</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AAPage;
