import React from 'react';
import { createStore } from 'zustand';
import { useStore } from 'zustand';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Box,
  Container,
  Typography,
  Button,
  TextField,
  Paper,
  AppBar,
  Toolbar,
  Alert,
  Divider,
  Grid,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Logout,
  Sync,
  Receipt,
  AccountBalance,
  TrendingUp,
  Insights,
  Timeline,
  Search,
  ShoppingCart,
  LocalOffer,
  LocalShipping,
  VerifiedUser,
  History,
  SmartToy,
  Hub
} from '@mui/icons-material';

// 1. Theme Configuration
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#4285F4' },
    secondary: { main: '#34A853' }, // green-ish accent
    info: { main: '#EA4335' }, // red accent
    background: { default: '#060913', paper: '#0F1626' },
    text: { primary: '#F1F5F9', secondary: '#94A3B8' }
  },
  typography: {
    fontFamily: 'Outfit, Inter, sans-serif',
    h5: { fontWeight: 700, letterSpacing: '-0.5px' },
    h6: { fontWeight: 600 }
  },
  shape: { borderRadius: 12 }
});

// 2. Types
interface TReDSInvoice {
  id: number;
  customer_id: number;
  invoice_number: string;
  buyer_pan: string;
  buyer_name: string;
  amount: number;
  tenure_days: number;
  issue_date: string;
  due_date: string;
  status: string;
}

interface Lender {
  lender_id: string;
  name: string;
  lender_type: string;
  base_interest_rate: number;
  max_loan_amount: number;
  min_credit_score: number;
}

interface Partner {
  partner_id: string;
  name: string;
  partner_type: string;
}

interface LoanApplication {
  id: number;
  customer_id: number;
  uli_reference: string;
  requested_amount: number;
  requested_tenure_months: number;
  purpose: string;
  status: string;
  selected_offer_id: number | null;
}

interface LoanOffer {
  id: number;
  application_id: number;
  lender_id: string;
  lender_name: string;
  offered_amount: number;
  interest_rate: number;
  tenure_months: number;
  processing_fee: number;
  monthly_installment: number;
  status: string;
}

interface AIRecommendation {
  suitability_score: number;
  dynamic_summary: string;
  recommended_offer_id: number | null;
  breakdown: string;
}

interface AuditLog {
  id: number;
  correlation_id: string;
  event_type: string;
  actor: string;
  message: string;
  details: string | null;
  timestamp: string;
}

// 3. Zustand TReDS Store
interface TReDSState {
  isAuthenticated: boolean;
  role: string | null;
  customerId: string;
  sellerPanInput: string;
  invoices: TReDSInvoice[];
  errorMessage: string | null;
  successMessage: string | null;
  isSyncing: boolean;
  isDiscounting: boolean;

  login: (role: string) => void;
  logout: () => void;
  setInput: (field: string, value: string) => void;
  syncInvoices: () => Promise<void>;
  fetchInvoices: () => Promise<void>;
  discountInvoice: (id: number) => Promise<void>;
}

const tredsStore = createStore<TReDSState>((set, get) => ({
  isAuthenticated: false,
  role: null,
  customerId: '125',
  sellerPanInput: 'ABCDE1234F',
  invoices: [],
  errorMessage: null,
  successMessage: null,
  isSyncing: false,
  isDiscounting: false,

  login: (role) => set({ isAuthenticated: true, role }),
  logout: () => set({ isAuthenticated: false, role: null, invoices: [] }),
  setInput: (field, value) => set({ [field]: value } as any),
  syncInvoices: async () => {
    set({ isSyncing: true, errorMessage: null, successMessage: null });
    try {
      const response = await fetch(`http://localhost:8096/treds/sync/${get().customerId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seller_pan: get().sellerPanInput })
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.message || 'Sync failed.');
      }

      const data = await response.json();
      set({ invoices: data, successMessage: 'TReDS registry invoices synced successfully.' });
    } catch (error: any) {
      set({ errorMessage: error.message });
    } finally {
      set({ isSyncing: false });
    }
  },
  fetchInvoices: async () => {
    try {
      const response = await fetch(`http://localhost:8096/treds/invoices/${get().customerId}`);
      if (response.ok) {
        const data = await response.json();
        set({ invoices: data });
      }
    } catch (e) {
      // Silent error
    }
  },
  discountInvoice: async (id) => {
    set({ isDiscounting: true, errorMessage: null, successMessage: null });
    try {
      const response = await fetch(`http://localhost:8096/treds/discount/${id}`, { method: 'POST' });
      if (!response.ok) throw new Error('Discounting flow failed.');
      set({ successMessage: 'Invoice successfully discounted. Working capital advanced.' });
      get().fetchInvoices();
    } catch (error: any) {
      set({ errorMessage: error.message });
    } finally {
      set({ isDiscounting: false });
    }
  }
}));

// 4. Zustand OCEN & ULI Store
interface OCENState {
  eligibility: {
    eligible: boolean;
    reason: string;
    max_eligible_amount: number;
    uli_reference: string;
  } | null;
  application: LoanApplication | null;
  offers: LoanOffer[];
  bestRateOfferId: number | null;
  bestAmountOfferId: number | null;
  comparisonNotes: string;
  aiAdvisor: AIRecommendation | null;
  lenders: Lender[];
  partners: Partner[];
  auditLogs: AuditLog[];
  isLoading: boolean;

  checkEligibility: (revenue: number, score: number, amount: number) => Promise<void>;
  applyLoan: (amount: number, tenure: number, purpose: string) => Promise<void>;
  acceptOffer: (offerId: number) => Promise<void>;
  disburseLoan: () => Promise<void>;
  fetchLendersAndPartners: () => Promise<void>;
  fetchAuditLogs: () => Promise<void>;
  resetCreditPortal: () => void;
}

const ocenStore = createStore<OCENState>((set, get) => ({
  eligibility: null,
  application: null,
  offers: [],
  bestRateOfferId: null,
  bestAmountOfferId: null,
  comparisonNotes: '',
  aiAdvisor: null,
  lenders: [],
  partners: [],
  auditLogs: [],
  isLoading: false,

  resetCreditPortal: () => set({
    eligibility: null,
    application: null,
    offers: [],
    bestRateOfferId: null,
    bestAmountOfferId: null,
    comparisonNotes: '',
    aiAdvisor: null
  }),

  checkEligibility: async (revenue, score, amount) => {
    set({ isLoading: true });
    try {
      const customerId = tredsStore.getState().customerId;
      const res = await fetch('http://localhost:8000/ocen/eligibility', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_id: parseInt(customerId) || 125,
          annual_revenue: revenue,
          credit_score: score,
          requested_amount: amount
        })
      });
      if (res.ok) {
        const data = await res.json();
        set({ eligibility: data });
        get().fetchAuditLogs();
      }
    } catch (e) {
      console.error(e);
    } finally {
      set({ isLoading: false });
    }
  },

  applyLoan: async (amount, tenure, purpose) => {
    set({ isLoading: true });
    try {
      const customerId = tredsStore.getState().customerId;
      const res = await fetch('http://localhost:8000/ocen/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_id: parseInt(customerId) || 125,
          requested_amount: amount,
          requested_tenure_months: tenure,
          purpose: purpose
        })
      });
      if (res.ok) {
        const appData = await res.json();
        set({ application: appData });

        // Fetch offers
        const offersRes = await fetch(`http://localhost:8000/ocen/applications/${appData.id}/offers`);
        if (offersRes.ok) {
          const offersData = await offersRes.json();
          set({ offers: offersData });
        }

        // Fetch Comparison
        const compRes = await fetch(`http://localhost:8000/ocen/offers/compare/${appData.id}`);
        if (compRes.ok) {
          const compData = await compRes.json();
          set({
            bestRateOfferId: compData.best_rate_offer_id,
            bestAmountOfferId: compData.best_amount_offer_id,
            comparisonNotes: compData.comparison_notes
          });
        }

        // Fetch AI recommendation
        const aiRes = await fetch(`http://localhost:8000/ocen/ai-advisor/${appData.id}`);
        if (aiRes.ok) {
          const aiData = await aiRes.json();
          set({ aiAdvisor: aiData });
        }

        get().fetchAuditLogs();
      }
    } catch (e) {
      console.error(e);
    } finally {
      set({ isLoading: false });
    }
  },

  acceptOffer: async (offerId) => {
    set({ isLoading: true });
    try {
      const res = await fetch('http://localhost:8000/ocen/offers/accept', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ offer_id: offerId })
      });
      if (res.ok) {
        const appData = await res.json();
        set({ application: appData });
        
        // Refresh offers list
        if (get().application) {
          const offersRes = await fetch(`http://localhost:8000/ocen/applications/${appData.id}/offers`);
          if (offersRes.ok) {
            const offersData = await offersRes.json();
            set({ offers: offersData });
          }
        }
        get().fetchAuditLogs();
      }
    } catch (e) {
      console.error(e);
    } finally {
      set({ isLoading: false });
    }
  },

  disburseLoan: async () => {
    const appRecord = get().application;
    if (!appRecord) return;
    set({ isLoading: true });
    try {
      const res = await fetch(`http://localhost:8000/ocen/disburse/${appRecord.id}`, {
        method: 'POST'
      });
      if (res.ok) {
        const appData = await res.json();
        set({ application: appData });
        get().fetchAuditLogs();
      }
    } catch (e) {
      console.error(e);
    } finally {
      set({ isLoading: false });
    }
  },

  fetchLendersAndPartners: async () => {
    try {
      const lendersRes = await fetch('http://localhost:8000/ocen/lenders');
      if (lendersRes.ok) {
        const lendersData = await lendersRes.json();
        set({ lenders: lendersData });
      }
      const partnersRes = await fetch('http://localhost:8000/ocen/partners');
      if (partnersRes.ok) {
        const partnersData = await partnersRes.json();
        set({ partners: partnersData });
      }
    } catch (e) {
      console.error(e);
    }
  },

  fetchAuditLogs: async () => {
    try {
      const res = await fetch('http://localhost:8000/ocen/audit-logs');
      if (res.ok) {
        const logsData = await res.json();
        set({ auditLogs: logsData });
      }
    } catch (e) {
      console.error(e);
    }
  }
}));

// Helper to format values as Lakhs
function formatLakhs(val: number): string {
  return `₹${(val / 100000).toFixed(2)} Lakhs`;
}

// Helper to format currency properly
function formatCurrency(val: number): string {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(val);
}

// 5. View Assemblies
export default function App() {
  const store = useStore(tredsStore);
  const ocen = useStore(ocenStore);
  const [localMobile, setLocalMobile] = React.useState('');
  const [activeTab, setActiveTab] = React.useState(0);

  // OCEN inputs state
  const [revenue, setRevenue] = React.useState('5000000');
  const [creditScore, setCreditScore] = React.useState('750');
  const [reqAmount, setReqAmount] = React.useState('1000000');
  const [loanPurpose, setLoanPurpose] = React.useState('Business expansion and raw material procurement');
  const [loanTenure, setLoanTenure] = React.useState('12');

  React.useEffect(() => {
    if (store.isAuthenticated) {
      store.fetchInvoices();
      ocen.fetchLendersAndPartners();
      ocen.fetchAuditLogs();
    }
  }, [store.isAuthenticated]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        
        {/* Navigation Toolbar */}
        <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
          <Toolbar>
            <Typography variant="h6" color="primary" sx={{ flexGrow: 1, fontWeight: '800' }}>
              PROJECT AAROHAN - ENTERPRISE CREDIT GATEWAY
            </Typography>
            {store.isAuthenticated && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Chip label={`Role: ${store.role}`} color="secondary" />
                <Button color="inherit" endIcon={<Logout />} onClick={store.logout}>Sign Out</Button>
              </Box>
            )}
          </Toolbar>
        </AppBar>

        {/* Global Notifications */}
        <Container maxWidth="md" sx={{ mt: 2 }}>
          {store.errorMessage && <Alert severity="error" onClose={() => tredsStore.setState({ errorMessage: null })}>{store.errorMessage}</Alert>}
          {store.successMessage && <Alert severity="success" onClose={() => tredsStore.setState({ successMessage: null })}>{store.successMessage}</Alert>}
        </Container>

        <Container sx={{ flexGrow: 1, py: 4 }}>
          
          {/* LOGIN WINDOW */}
          {!store.isAuthenticated ? (
            <Paper elevation={4} sx={{ p: 4, width: '100%', maxWidth: 440, mx: 'auto', mt: 8, border: '1px solid rgba(255,255,255,0.05)' }}>
              <Typography variant="h5" align="center" gutterBottom>
                Identity Portal Verification
              </Typography>
              <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
                Simulate login for credit intelligence dashboard
              </Typography>
              <TextField
                fullWidth
                label="Staff Mobile Access"
                value={localMobile}
                onChange={(e) => setLocalMobile(e.target.value)}
                placeholder="e.g. 9876543210 (RM) or 9988776655 (Client)"
                sx={{ mb: 3 }}
              />
              <Button
                fullWidth
                size="large"
                variant="contained"
                onClick={() => {
                  const role = localMobile === '9876543210' ? 'RELATIONSHIP_MANAGER' : 'CUSTOMER';
                  store.login(role);
                }}
              >
                Sign In
              </Button>
            </Paper>
          ) : (
            // MAIN DASHBOARD LAYOUT
            <Box>
              <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                <Tabs value={activeTab} onChange={handleTabChange} textColor="primary" indicatorColor="primary">
                  <Tab label="TReDS Receivables Discounting" />
                  <Tab label="OCEN & ULI Embedded Credit" />
                </Tabs>
              </Box>

              {ocen.isLoading && <LinearProgress color="primary" sx={{ mb: 2 }} />}

              {activeTab === 0 ? (
                // TAB 0: TReDS Receivables
                <Box>
                  {/* SYNC FORM */}
                  <Paper sx={{ p: 3, mb: 4, border: '1px solid rgba(255,255,255,0.05)' }}>
                    <Typography variant="h6" gutterBottom color="primary">TReDS Invoices Sync Panel</Typography>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={12} sm={4}>
                        <TextField fullWidth label="Scanned Customer ID" value={store.customerId} onChange={(e) => store.setInput('customerId', e.target.value)} />
                      </Grid>
                      <Grid item xs={12} sm={5}>
                        <TextField fullWidth label="Seller PAN Code" value={store.sellerPanInput} onChange={(e) => store.setInput('sellerPanInput', e.target.value)} placeholder="e.g. ABCDE1234F" />
                      </Grid>
                      <Grid item xs={12} sm={3}>
                        <Button fullWidth size="large" variant="contained" startIcon={<Sync />} onClick={store.syncInvoices} disabled={store.isSyncing}>
                          {store.isSyncing ? 'Syncing...' : 'Sync TReDS Invoices'}
                        </Button>
                      </Grid>
                    </Grid>
                  </Paper>

                  {store.invoices.length > 0 ? (
                    <Grid container spacing={3}>
                      {/* INVOICES GRID */}
                      <Grid item xs={12} md={7}>
                        <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.05)', height: '100%' }}>
                          <Typography variant="h6" color="primary" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            <Receipt /> Scanned TReDS Receivables Invoices
                          </Typography>
                          <Divider sx={{ my: 1.5 }} />
                          <TableContainer>
                            <Table size="small">
                              <TableHead>
                                <TableRow>
                                  <TableCell>Invoice Number</TableCell>
                                  <TableCell>Buyer Name</TableCell>
                                  <TableCell>Amount</TableCell>
                                  <TableCell>Tenure</TableCell>
                                  <TableCell>Status</TableCell>
                                  <TableCell>Action</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {store.invoices.map((inv) => (
                                  <TableRow key={inv.id}>
                                    <TableCell>{inv.invoice_number}</TableCell>
                                    <TableCell>{inv.buyer_name}</TableCell>
                                    <TableCell>{formatLakhs(inv.amount)}</TableCell>
                                    <TableCell>{inv.tenure_days} Days</TableCell>
                                    <TableCell>
                                      <Chip label={inv.status} color={inv.status === 'DISCOUNTED' ? 'success' : 'primary'} size="small" />
                                    </TableCell>
                                    <TableCell>
                                      {inv.status === 'ELIGIBLE' && store.role === 'RELATIONSHIP_MANAGER' && (
                                        <Button size="small" variant="contained" color="secondary" onClick={() => store.discountInvoice(inv.id)} disabled={store.isDiscounting}>
                                          Discount
                                        </Button>
                                      )}
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </Paper>
                      </Grid>

                      {/* DETAILS & AI RECEIVABLES PANEL */}
                      <Grid item xs={12} md={5}>
                        <Grid container spacing={3}>
                          <Grid item xs={12}>
                            <Card sx={{ bgcolor: '#121829', border: '1px solid rgba(255,255,255,0.05)' }}>
                              <CardContent>
                                <Typography variant="subtitle2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                  <TrendingUp fontSize="small" /> Working Capital Impact
                                </Typography>
                                <Typography variant="h5" sx={{ mt: 1 }} color="primary" fontWeight="bold">
                                  +12.4 Days Reduced
                                </Typography>
                                <Typography variant="caption" color="text.secondary">Cash Conversion cycle optimization</Typography>
                              </CardContent>
                            </Card>
                          </Grid>
                          <Grid item xs={12}>
                            <Paper sx={{ p: 3, border: '1px solid rgba(66,133,244,0.3)', bgcolor: 'rgba(66,133,244,0.04)' }}>
                              <Typography variant="subtitle2" color="primary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                                <Insights fontSize="small" /> Gemini AI Supply Chain Finance Advisor
                              </Typography>
                              <Divider sx={{ my: 1.5 }} />
                              <Typography variant="body2" color="text.secondary">
                                "TReDS registry sync completes. Invoices under Tata Motors and Reliance Retail qualify for immediate discounting. Buyer credit scores stand at AA/AAA with average settlement cycles of 45-60 days."
                              </Typography>
                            </Paper>
                          </Grid>
                        </Grid>
                      </Grid>
                    </Grid>
                  ) : (
                    <Paper sx={{ p: 4, textAlign: 'center', border: '1px dashed rgba(255,255,255,0.08)' }}>
                      <ShoppingCart sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
                      <Typography variant="body2" color="text.secondary">Provide customer ID and Seller PAN to synchronize trade receivables invoices from TReDS registry.</Typography>
                    </Paper>
                  )}
                </Box>
              ) : (
                // TAB 1: OCEN & ULI Embedded Credit
                <Box>
                  <Grid container spacing={3}>
                    {/* LEFT PANEL: ELIGIBILITY & DISCOVERY */}
                    <Grid item xs={12} md={7}>
                      <Grid container spacing={3}>
                        
                        {/* 1. ELIGIBILITY CHECKER */}
                        <Grid item xs={12}>
                          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.05)' }}>
                            <Typography variant="h6" gutterBottom color="primary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <VerifiedUser /> 1. ULI Consent & Eligibility Check
                            </Typography>
                            <Divider sx={{ my: 1.5 }} />
                            <Grid container spacing={2}>
                              <Grid item xs={12} sm={4}>
                                <TextField fullWidth label="Annual Revenue (₹)" value={revenue} onChange={(e) => setRevenue(e.target.value)} />
                              </Grid>
                              <Grid item xs={12} sm={4}>
                                <TextField fullWidth label="Credit Score" value={creditScore} onChange={(e) => setCreditScore(e.target.value)} />
                              </Grid>
                              <Grid item xs={12} sm={4}>
                                <TextField fullWidth label="Loan Request (₹)" value={reqAmount} onChange={(e) => setReqAmount(e.target.value)} />
                              </Grid>
                            </Grid>
                            <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                              <Button variant="contained" color="primary" onClick={() => ocen.checkEligibility(parseFloat(revenue), parseInt(creditScore), parseFloat(reqAmount))}>
                                Verify via ULI Gateway
                              </Button>
                              <Button variant="outlined" onClick={ocen.resetCreditPortal}>Reset Portal</Button>
                            </Box>

                            {ocen.eligibility && (
                              <Box sx={{ mt: 2.5, p: 2, bgcolor: ocen.eligibility.eligible ? 'rgba(52,168,83,0.08)' : 'rgba(234,67,53,0.08)', border: ocen.eligibility.eligible ? '1px solid #34A853' : '1px solid #EA4335', borderRadius: 2 }}>
                                <Typography variant="subtitle1" fontWeight="bold" color={ocen.eligibility.eligible ? 'secondary' : 'info'}>
                                  {ocen.eligibility.eligible ? 'ELIGIBLE' : 'INELIGIBLE'}
                                </Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                                  {ocen.eligibility.reason}
                                </Typography>
                                {ocen.eligibility.eligible && (
                                  <Box sx={{ mt: 1 }}>
                                    <Typography variant="body2" color="text.primary"><strong>Max Offer Ceiling:</strong> {formatCurrency(ocen.eligibility.max_eligible_amount)}</Typography>
                                    <Typography variant="caption" color="text.secondary"><strong>ULI Ref:</strong> {ocen.eligibility.uli_reference}</Typography>
                                  </Box>
                                )}
                              </Box>
                            )}
                          </Paper>
                        </Grid>

                        {/* 2. LOAN DISCOVERY / APPLICATION */}
                        {ocen.eligibility?.eligible && (
                          <Grid item xs={12}>
                            <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.05)' }}>
                              <Typography variant="h6" gutterBottom color="primary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <AccountBalance /> 2. OCEN Digital Loan Marketplace Application
                              </Typography>
                              <Divider sx={{ my: 1.5 }} />
                              <Grid container spacing={2}>
                                <Grid item xs={12} sm={8}>
                                  <TextField fullWidth label="Lending Purpose" value={loanPurpose} onChange={(e) => setLoanPurpose(e.target.value)} />
                                </Grid>
                                <Grid item xs={12} sm={4}>
                                  <TextField fullWidth label="Tenure (Months)" value={loanTenure} onChange={(e) => setLoanTenure(e.target.value)} />
                                </Grid>
                              </Grid>
                              <Button variant="contained" color="secondary" sx={{ mt: 2 }} onClick={() => ocen.applyLoan(parseFloat(reqAmount), parseInt(loanTenure), loanPurpose)}>
                                Query Lenders Registry
                              </Button>
                            </Paper>
                          </Grid>
                        )}

                        {/* 3. OFFERS & COMPARISON */}
                        {ocen.offers.length > 0 && (
                          <Grid item xs={12}>
                            <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.05)' }}>
                              <Typography variant="h6" gutterBottom color="primary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <LocalOffer /> 3. Received Offers & Comparison Screen
                              </Typography>
                              <Divider sx={{ my: 1.5 }} />
                              <TableContainer>
                                <Table size="small">
                                  <TableHead>
                                    <TableRow>
                                      <TableCell>Lender</TableCell>
                                      <TableCell>Amount</TableCell>
                                      <TableCell>Rate (APR)</TableCell>
                                      <TableCell>EMI (Monthly)</TableCell>
                                      <TableCell>Proc. Fee</TableCell>
                                      <TableCell>Status</TableCell>
                                      <TableCell>Decision</TableCell>
                                    </TableRow>
                                  </TableHead>
                                  <TableBody>
                                    {ocen.offers.map((offer) => {
                                      const isBestRate = offer.id === ocen.bestRateOfferId;
                                      const isBestAmount = offer.id === ocen.bestAmountOfferId;
                                      return (
                                        <TableRow key={offer.id}>
                                          <TableCell>
                                            {offer.lender_name}
                                            {isBestRate && <Chip label="Best Rate" size="small" color="secondary" sx={{ ml: 1, height: 18 }} />}
                                          </TableCell>
                                          <TableCell>{formatCurrency(offer.offered_amount)}</TableCell>
                                          <TableCell>{offer.interest_rate}%</TableCell>
                                          <TableCell>{formatCurrency(offer.monthly_installment)}</TableCell>
                                          <TableCell>{formatCurrency(offer.processing_fee)}</TableCell>
                                          <TableCell>
                                            <Chip label={offer.status} color={offer.status === 'ACCEPTED' ? 'success' : 'primary'} size="small" />
                                          </TableCell>
                                          <TableCell>
                                            {ocen.application?.status === 'OFFERS_GENERATED' && (
                                              <Button size="small" variant="outlined" onClick={() => ocen.acceptOffer(offer.id)}>
                                                Select
                                              </Button>
                                            )}
                                          </TableCell>
                                        </TableRow>
                                      );
                                    })}
                                  </TableBody>
                                </Table>
                              </TableContainer>
                              {ocen.comparisonNotes && (
                                <Box sx={{ mt: 2, p: 1.5, bgcolor: '#121829', border: '1px solid rgba(255,255,255,0.05)', borderRadius: 1.5 }}>
                                  <Typography variant="body2" color="text.secondary">
                                    <strong>Engine Analyser:</strong> {ocen.comparisonNotes}
                                  </Typography>
                                </Box>
                              )}
                            </Paper>
                          </Grid>
                        )}

                      </Grid>
                    </Grid>

                    {/* RIGHT PANEL: TIMELINE & AI ASSISTANT */}
                    <Grid item xs={12} md={5}>
                      <Grid container spacing={3}>
                        
                        {/* 1. AI LENDING ASSISTANT PANEL */}
                        {ocen.aiAdvisor && (
                          <Grid item xs={12}>
                            <Paper sx={{ p: 3, border: '1px solid rgba(66,133,244,0.4)', bgcolor: 'rgba(66,133,244,0.04)' }}>
                              <Typography variant="subtitle2" color="primary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                                <SmartToy fontSize="small" /> Gemini ULI Credit Intelligence
                              </Typography>
                              <Divider sx={{ my: 1.5 }} />
                              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                                <Typography variant="body2" color="text.secondary">Suitability Index Score</Typography>
                                <Typography variant="body2" fontWeight="bold" color="secondary">{ocen.aiAdvisor.suitability_score}%</Typography>
                              </Box>
                              <Typography variant="body2" fontWeight="bold" color="text.primary" sx={{ mb: 1 }}>
                                {ocen.aiAdvisor.dynamic_summary}
                              </Typography>
                              <Typography variant="body2" color="text.secondary" style={{ whiteSpace: 'pre-line' }}>
                                {ocen.aiAdvisor.breakdown}
                              </Typography>
                            </Paper>
                          </Grid>
                        )}

                        {/* 2. LOAN JOURNEY TIMELINE */}
                        {ocen.application && (
                          <Grid item xs={12}>
                            <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.05)' }}>
                              <Typography variant="h6" color="primary" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <Timeline /> Loan Application Status Tracker
                              </Typography>
                              <Divider sx={{ my: 1.5 }} />
                              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                  <Typography variant="body2"><strong>ULI Ref:</strong> {ocen.application.uli_reference}</Typography>
                                  <Chip label={ocen.application.status} color="success" size="small" />
                                </Box>
                                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, pl: 1, borderLeft: '2px solid rgba(255,255,255,0.1)' }}>
                                  <Box sx={{ opacity: ocen.application.status !== 'APPLIED' ? 1 : 0.5 }}>
                                    <Typography variant="body2">✓ <strong>ULI Reference Initialized</strong></Typography>
                                  </Box>
                                  <Box sx={{ opacity: ['OFFERS_GENERATED', 'ACCEPTED', 'DISBURSED'].includes(ocen.application.status) ? 1 : 0.5 }}>
                                    <Typography variant="body2">✓ <strong>OCEN Market Offers Fetched</strong></Typography>
                                  </Box>
                                  <Box sx={{ opacity: ['ACCEPTED', 'DISBURSED'].includes(ocen.application.status) ? 1 : 0.5 }}>
                                    <Typography variant="body2">✓ <strong>Offer Accepted by Borrower</strong></Typography>
                                  </Box>
                                  <Box sx={{ opacity: ocen.application.status === 'DISBURSED' ? 1 : 0.5 }}>
                                    <Typography variant="body2">✓ <strong>Funds Disbursed to Bank Account</strong></Typography>
                                  </Box>
                                </Box>

                                {ocen.application.status === 'ACCEPTED' && (
                                  <Button fullWidth variant="contained" color="secondary" onClick={ocen.disburseLoan}>
                                    Disburse Loan Instantly
                                  </Button>
                                )}
                              </Box>
                            </Paper>
                          </Grid>
                        )}

                        {/* 3. PARTNERS & LENDERS REGISTRY */}
                        <Grid item xs={12}>
                          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.05)' }}>
                            <Typography variant="h6" color="primary" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Hub /> OCEN Network Partner Directory
                            </Typography>
                            <Divider sx={{ my: 1.5 }} />
                            <Grid container spacing={2}>
                              <Grid item xs={6}>
                                <Typography variant="subtitle2" color="primary">Active Lenders</Typography>
                                <List dense>
                                  {ocen.lenders.map(l => (
                                    <ListItem key={l.lender_id} disableGutters>
                                      <ListItemText primary={l.name} secondary={`${l.lender_type} | base: ${l.base_interest_rate}%`} />
                                    </ListItem>
                                  ))}
                                </List>
                              </Grid>
                              <Grid item xs={6}>
                                <Typography variant="subtitle2" color="primary">Partners (LSPs)</Typography>
                                <List dense>
                                  {ocen.partners.map(p => (
                                    <ListItem key={p.partner_id} disableGutters>
                                      <ListItemText primary={p.name} secondary={p.partner_type} />
                                    </ListItem>
                                  ))}
                                </List>
                              </Grid>
                            </Grid>
                          </Paper>
                        </Grid>

                        {/* 4. AUDIT TRAIL LOGS */}
                        <Grid item xs={12}>
                          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.05)', maxHeight: 250, overflowY: 'auto' }}>
                            <Typography variant="h6" color="primary" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <History /> Lending Gateway Audit Logs
                            </Typography>
                            <Divider sx={{ my: 1.5 }} />
                            <List dense>
                              {ocen.auditLogs.map(log => (
                                <ListItem key={log.id} disableGutters>
                                  <ListItemText primary={`[${log.event_type}] ${log.message}`} secondary={`${new Date(log.timestamp).toLocaleString()} | Actor: ${log.actor}`} />
                                </ListItem>
                              ))}
                            </List>
                          </Paper>
                        </Grid>

                      </Grid>
                    </Grid>
                  </Grid>
                </Box>
              )}

            </Box>
          )}

        </Container>
      </Box>
    </ThemeProvider>
  );
}
