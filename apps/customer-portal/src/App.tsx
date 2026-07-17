import React from 'react';
import { createStore } from 'zustand';
import { useStore } from 'zustand';
import CustomerOnboardingPage from './pages/CustomerOnboardingPage';
import CKYCPage from './pages/CKYCPage';
import GSTPage from './pages/GSTPage';
import AAPage from './pages/AAPage';
import EPFOPage from './pages/EPFOPage';
import MCAPage from './pages/MCAPage';
import CAMPage from './pages/CAMPage';
import ExecutiveCommandCenterPage from './pages/ExecutiveCommandCenterPage';
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
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  IconButton,
  Drawer,
  Avatar,
  CircularProgress,
  Snackbar,
  Stack,
  Stepper,
  Step,
  StepLabel,
  LinearProgress
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  People,
  PersonSearch,
  Receipt,
  AccountBalance,
  WorkOutline,
  Business,
  Assessment,
  Memory,
  Description,
  ShoppingCart,
  Gavel,
  BarChart,
  SettingsInputComponent,
  FolderZip,
  SupervisorAccount,
  Settings as SettingsIcon,
  Brightness4,
  Brightness7,
  Notifications,
  VerifiedUser,
  History,
  TrendingUp,
  SmartToy,
  Logout,
  VpnKey,
  PlayArrow,
  CheckCircle,
  Pause,
  Refresh,
  Speed,
  ListAlt,
  Stop,
  Check,
  ErrorOutline
} from '@mui/icons-material';

// ----------------------------------------------------
// 1. ZUSTAND CENTRAL STATE MANAGEMENT
// ----------------------------------------------------
interface UserProfile {
  id: number;
  mobile_number: string;
  email: string | null;
  full_name: string;
  role: string;
  department?: string;
  branch?: string;
  avatar?: string;
  permissions: string[];
}

interface UIState {
  themeMode: 'light' | 'dark';
  activePage: string;
  activeDataset: string;
  notification: { open: boolean; message: string; severity: 'success' | 'info' | 'warning' | 'error' } | null;
  
  // Auth state
  isAuthenticated: boolean;
  token: string | null;
  user: UserProfile | null;
  isLoading: boolean;
  
  // Simulation Active Selection State
  activePersona: string;
  activeScenario: string;
  
  toggleTheme: () => void;
  setActivePage: (page: string) => void;
  setActiveDataset: (dataset: string) => void;
  showNotification: (message: string, severity?: 'success' | 'info' | 'warning' | 'error') => void;
  closeNotification: () => void;
  
  // Auth actions
  login: (mobile: string, password: string) => Promise<boolean>;
  logout: () => void;
  
  // Simulation actions
  setSimulation: (persona: string, scenario: string) => Promise<void>;
}

const uiStore = createStore<UIState>((set, get) => ({
  themeMode: 'dark',
  activePage: 'Dashboard',
  activeDataset: 'msme',
  notification: null,
  
  isAuthenticated: false,
  token: null,
  user: null,
  isLoading: false,
  
  activePersona: 'Priya Textile Works',
  activeScenario: 'Healthy Business',
  
  toggleTheme: () => set((state) => ({ themeMode: state.themeMode === 'light' ? 'dark' : 'light' })),
  setActivePage: (page) => set({ activePage: page }),
  setActiveDataset: (dataset) => set({ activeDataset: dataset }),
  showNotification: (message, severity = 'success') => set({ notification: { open: true, message, severity } }),
  closeNotification: () => set({ notification: null }),
  
  login: async (mobile, password) => {
    set({ isLoading: true });
    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile_number: mobile, password })
      });
      
      if (!response.ok) {
        throw new Error('Authentication failed. Check your credentials.');
      }
      
      const tokenData = await response.json();
      
      const meResponse = await fetch('http://localhost:8000/auth/me', {
        headers: { 'Authorization': `Bearer ${tokenData.access_token}` }
      });
      
      if (!meResponse.ok) {
        throw new Error('Failed to retrieve user profile.');
      }
      
      const profile = await meResponse.json();
      
      try {
        const controlRes = await fetch('http://localhost:8090/ese/control');
        if (controlRes.ok) {
          const controlState = await controlRes.json();
          set({
            activePersona: controlState.active_persona,
            activeScenario: controlState.active_scenario,
            activeDataset: controlState.active_dataset
          });
        }
      } catch (e) {
        // Silent error
      }
      
      set({
        isAuthenticated: true,
        token: tokenData.access_token,
        user: {
          ...profile,
          department: profile.department || 'Operations',
          branch: profile.branch || 'Mumbai HQ',
          avatar: profile.avatar || '/assets/avatars/default.png'
        },
        activePage: 'Dashboard'
      });
      
      get().showNotification(`Welcome back, ${profile.full_name}!`, 'success');
      return true;
    } catch (error: any) {
      get().showNotification(error.message, 'error');
      return false;
    } finally {
      set({ isLoading: false });
    }
  },
  
  logout: () => {
    set({
      isAuthenticated: false,
      token: null,
      user: null,
      activePage: 'Dashboard'
    });
    get().showNotification('You have logged out successfully.', 'info');
  },
  
  setSimulation: async (persona, scenario) => {
    set({ isLoading: true });
    try {
      await fetch('http://localhost:8090/ese/control/persona', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ persona })
      });
      
      await fetch('http://localhost:8090/ese/control/scenario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario })
      });
      
      set({ activePersona: persona, activeScenario: scenario });
      get().showNotification(`Lending twin configured: ${persona} - ${scenario}`, 'success');
    } catch (e: any) {
      get().showNotification(`Sandbox sync failed: ${e.message}`, 'warning');
      set({ activePersona: persona, activeScenario: scenario });
    } finally {
      set({ isLoading: false });
    }
  }
}));

// ----------------------------------------------------
// 2. DESIGN SYSTEM REUSABLE COMPONENTS
// ----------------------------------------------------

interface MetricCardProps {
  title: string;
  value: string | number;
  subtext?: string;
  trend?: string;
  trendPositive?: boolean;
  icon: React.ReactNode;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtext, trend, trendPositive = true, icon }) => (
  <Paper elevation={1} sx={{ p: 3, height: '100%', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
      <Typography variant="body2" color="text.secondary" fontWeight="500">
        {title}
      </Typography>
      <Box sx={{ color: 'primary.main', opacity: 0.8 }}>{icon}</Box>
    </Box>
    <Typography variant="h4" fontWeight="700" sx={{ mb: 1 }}>
      {value}
    </Typography>
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      {trend && (
        <Typography variant="caption" fontWeight="bold" color={trendPositive ? 'success.main' : 'error.main'}>
          {trend}
        </Typography>
      )}
      {subtext && (
        <Typography variant="caption" color="text.secondary">
          {subtext}
        </Typography>
      )}
    </Box>
  </Paper>
);

interface StatusBadgeProps {
  status: string;
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getBadgeConfig = (s: string) => {
    switch (s.toUpperCase()) {
      case 'APPROVED':
      case 'ACTIVE':
      case 'SUCCESS':
      case 'COMPLETED':
      case 'FILED':
        return { color: 'success' as const, label: s };
      case 'REJECTED':
      case 'BLACKLISTED':
      case 'ERROR':
      case 'FAILED':
        return { color: 'error' as const, label: s };
      case 'PENDING':
      case 'STRESSED':
      case 'RUNNING':
        return { color: 'warning' as const, label: s };
      default:
        return { color: 'primary' as const, label: s };
    }
  };
  const config = getBadgeConfig(status);
  return <Chip label={config.label} color={config.color} size="small" variant="outlined" />;
};

// ----------------------------------------------------
// 3. PAGES RENDER
// ----------------------------------------------------

const DashboardPage = () => {
  const ui = useStore(uiStore);
  return (
    <Box>
      <Typography variant="h5" color="text.primary" fontWeight="bold" sx={{ mb: 1 }}>
        Enterprise Overview Dashboard
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
        Real-time metrics, active underwriting pipelines, and simulation boundaries.
      </Typography>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard title="Total Customers" value="1,284" trend="+12%" subtext="vs last quarter" icon={<People />} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard title="Loan Applications" value="342" trend="+8%" subtext="active appraisals" icon={<Description />} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard title="Approval Rate" value="84%" trend="Optimal" trendPositive={true} subtext="policy compliance" icon={<VerifiedUser />} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard title="Portfolio Value" value="₹18.4 Cr" trend="+15%" subtext="Active outstanding" icon={<TrendingUp />} />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Recent Loan Activity Feed
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Borrower Name</TableCell>
                    <TableCell>Requested Limit</TableCell>
                    <TableCell>FHC Score</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>Priya Textile Works</TableCell>
                    <TableCell>₹25,000,000</TableCell>
                    <TableCell>85/100</TableCell>
                    <TableCell><StatusBadge status="APPROVED" /></TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>GreenAgro Cooperative</TableCell>
                    <TableCell>₹15,000,000</TableCell>
                    <TableCell>52/100</TableCell>
                    <TableCell><StatusBadge status="PENDING" /></TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>QuickLogistics</TableCell>
                    <TableCell>₹8,000,000</TableCell>
                    <TableCell>32/100</TableCell>
                    <TableCell><StatusBadge status="REJECTED" /></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Lending Twin Health Status
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2" color="text.secondary">Active dataset</Typography>
                <Typography variant="body2" fontWeight="bold" color="primary">{ui.activeDataset}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2" color="text.secondary">Simulation status</Typography>
                <Typography variant="body2" fontWeight="bold" color="success.main">RUNNING</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2" color="text.secondary">Active Persona</Typography>
                <Typography variant="body2" fontWeight="bold" color="secondary.main">{ui.activePersona}</Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

// Simulation Management Page Component
const SimulationPage = () => {
  const ui = useStore(uiStore);

  const mockPersonas = [
    { name: 'Priya Textile Works', industry: 'Manufacturing', segment: 'Exporter', location: 'Surat, Gujarat', turnover: '₹4.5 Cr', rating: 'A+', score: '82/100' },
    { name: 'GreenAgro Cooperative', industry: 'Agriculture', segment: 'Enterprise', location: 'Nashik, Maharashtra', turnover: '₹2.8 Cr', rating: 'BBB', score: '64/100' },
    { name: 'QuickLogistics Services', industry: 'Logistics', segment: 'Service Provider', location: 'Pune, Maharashtra', turnover: '₹8.4 Cr', rating: 'AA', score: '91/100' },
    { name: 'SparkTech Solutions', industry: 'Services', segment: 'Startup', location: 'Bangalore, Karnataka', turnover: '₹95L', rating: 'B-', score: '48/100' }
  ];

  const mockScenarios = [
    { id: 'Healthy Business', desc: 'Consistent filings, positive balances, zero fraud warnings.' },
    { id: 'High Growth', desc: 'Spiking GSTR-1 returns, low inventory storage cycles, request limit expansion.' },
    { id: 'Seasonal Business', desc: 'Predictable drop in working capital during monsoon quarter.' },
    { id: 'Cash Flow Stress', desc: 'Overdue receivable collections, high outstanding interest burdens.' },
    { id: 'GST Default', desc: 'Delayed GST returns for 3 successive filing sessions.' },
    { id: 'EPFO Default', desc: 'Pending corporate employee contribution deposits.' },
    { id: 'RBI Blacklisted', desc: 'Company listed on RBI defaulters central registry database.' }
  ];

  const [selectedPersona, setSelectedPersona] = React.useState(ui.activePersona);
  const [selectedScenario, setSelectedScenario] = React.useState(ui.activeScenario);

  const steps = [
    'Onboarding', 'CKYC Verification', 'GST Audit', 'Account Aggregator Sync', 
    'EPFO Check', 'MCA Filings', 'FHC Appraisal', 'AI Credit Underwriting', 
    'Fraud Verification', 'OCEN Marketplace', 'CAM Output'
  ];

  return (
    <Box>
      <Typography variant="h5" color="text.primary" fontWeight="bold" sx={{ mb: 1 }}>
        Enterprise Simulation Engine Dashboard
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
        Configure customer profiles, align macro-risk stress tests, and trace simulated underwriting pipelines.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              1. Choose Target Customer Persona
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            <Stack spacing={2}>
              {mockPersonas.map((p) => (
                <Card 
                  key={p.name} 
                  variant="outlined" 
                  onClick={() => setSelectedPersona(p.name)}
                  sx={{ 
                    cursor: 'pointer',
                    borderColor: selectedPersona === p.name ? 'primary.main' : 'rgba(255,255,255,0.08)',
                    bgcolor: selectedPersona === p.name ? 'rgba(66,133,244,0.04)' : 'transparent'
                  }}
                >
                  <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="subtitle2" fontWeight="bold">{p.name}</Typography>
                      <Chip label={p.rating} color="secondary" size="small" />
                    </Box>
                    <Grid container spacing={1}>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">Industry: {p.industry}</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">Turnover: {p.turnover}</Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              ))}
            </Stack>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              2. Select Stress Testing Business Scenario
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            <Stack spacing={2}>
              {mockScenarios.map((sc) => (
                <Card 
                  key={sc.id} 
                  variant="outlined" 
                  onClick={() => setSelectedScenario(sc.id)}
                  sx={{ 
                    cursor: 'pointer',
                    borderColor: selectedScenario === sc.id ? 'primary.main' : 'rgba(255,255,255,0.08)',
                    bgcolor: selectedScenario === sc.id ? 'rgba(66,133,244,0.04)' : 'transparent'
                  }}
                >
                  <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                    <Typography variant="subtitle2" fontWeight="bold" gutterBottom>{sc.id}</Typography>
                    <Typography variant="caption" color="text.secondary">{sc.desc}</Typography>
                  </CardContent>
                </Card>
              ))}
            </Stack>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 4, border: '1px solid rgba(66,133,244,0.3)', bgcolor: 'rgba(66,133,244,0.02)', borderRadius: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Box>
                <Typography variant="h6" fontWeight="bold">Active Simulation Launcher Preview</Typography>
                <Typography variant="caption" color="text.secondary">
                  Configure sandbox parameters for all downstream API endpoints.
                </Typography>
              </Box>
              <Button 
                variant="contained" 
                size="large" 
                startIcon={<PlayArrow />}
                onClick={() => ui.setSimulation(selectedPersona, selectedScenario)}
              >
                Activate Simulation
              </Button>
            </Box>

            <Grid container spacing={4} sx={{ mb: 4 }}>
              <Grid item xs={6} md={3}>
                <Typography variant="caption" color="text.secondary">Selected Customer Profile</Typography>
                <Typography variant="body2" fontWeight="bold">{selectedPersona}</Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography variant="caption" color="text.secondary">Macro Scenario</Typography>
                <Typography variant="body2" fontWeight="bold" color="secondary.main">{selectedScenario}</Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography variant="caption" color="text.secondary">Integration Sandbox</Typography>
                <Typography variant="body2" fontWeight="bold">CONNECTED</Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography variant="caption" color="text.secondary">Target Outcome</Typography>
                <Typography variant="body2" fontWeight="bold">
                  {selectedScenario === 'Healthy Business' ? 'Limits Approved' : 'Refer for Manual Audit'}
                </Typography>
              </Grid>
            </Grid>

            <Divider sx={{ my: 3 }} />

            <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>Simulation Journey Track</Typography>
            <Box sx={{ width: '100%', overflowX: 'auto', py: 2 }}>
              <Stepper activeStep={0} alternativeLabel>
                {steps.map((label) => (
                  <Step key={label}>
                    <StepLabel>{label}</StepLabel>
                  </Step>
                ))}
              </Stepper>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

// Lending Workflow Orchestrator Page (Onboarding View)
const OrchestratorPage = () => {
  const ui = useStore(uiStore);
  const [activeStep, setActiveStep] = React.useState(0);
  const [workflowStatus, setWorkflowStatus] = React.useState<'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED'>('PENDING');
  const [logs, setLogs] = React.useState<Array<{ time: string; msg: string; status: string }>>([]);

  const workflowSteps = [
    { name: 'Login Check', desc: 'Secure RM session validation.' },
    { name: 'Onboarding Registry', desc: 'Customer KYC registration file initialization.' },
    { name: 'CKYC Search', desc: 'Queries Central Registry matching PAN.' },
    { name: 'GST Audit Sync', desc: 'Sync GSTR returns history.' },
    { name: 'AA Banking Sync', desc: 'Sync cash ledger accounts.' },
    { name: 'EPFO Sync', desc: 'Validate employee pf distributions.' },
    { name: 'MCA Registry Verify', desc: 'Check registered corporate status.' },
    { name: 'FHC Scoring', desc: 'Compute Financial Health Score.' },
    { name: 'AI Credit Decision', desc: 'Run Gemini AI appraisal rules.' },
    { name: 'CAM Load', desc: 'Generate credit memorandum.' },
    { name: 'OCEN Marketplace', desc: 'Generate partner lender loan offers.' }
  ];

  const triggerWorkflow = async () => {
    setWorkflowStatus('RUNNING');
    setLogs([]);
    
    // Simulate orchestration step-by-step
    for (let i = 0; i < workflowSteps.length; i++) {
      setActiveStep(i);
      const step = workflowSteps[i];
      setLogs((prev) => [
        ...prev,
        {
          time: new Date().toLocaleTimeString(),
          msg: `Orchestrator invoking step: ${step.name} (${step.desc})`,
          status: 'RUNNING'
        }
      ]);
      
      await new Promise((resolve) => setTimeout(resolve, 800));
      
      setLogs((prev) => [
        ...prev,
        {
          time: new Date().toLocaleTimeString(),
          msg: `Step ${step.name} completed successfully. Business events published.`,
          status: 'SUCCESS'
        }
      ]);
    }
    
    setWorkflowStatus('COMPLETED');
    uiStore.getState().showNotification('Lending Journey Workflow Orchestrated successfully!', 'success');
  };

  const cancelWorkflow = () => {
    setWorkflowStatus('PENDING');
    setActiveStep(0);
    setLogs((prev) => [...prev, { time: new Date().toLocaleTimeString(), msg: 'Workflow execution cancelled by administrator.', status: 'ERROR' }]);
  };

  return (
    <Box>
      <Typography variant="h5" color="text.primary" fontWeight="bold" sx={{ mb: 1 }}>
        Enterprise Lending Workflow Orchestrator
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
        Coordinate every module of the MSME lending twin sequentially. Ensures compliance and transactional consistency.
      </Typography>

      <Grid container spacing={3}>
        {/* Controls and Stats */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2, height: '100%' }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Workflow Status Console
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            
            <Box sx={{ mb: 3 }}>
              <Typography variant="caption" color="text.secondary">Current Execution State</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                <StatusBadge status={workflowStatus} />
                {workflowStatus === 'RUNNING' && <CircularProgress size={16} />}
              </Box>
            </Box>

            <Box sx={{ mb: 3 }}>
              <Typography variant="caption" color="text.secondary">Progress completeness</Typography>
              <LinearProgress 
                variant="determinate" 
                value={workflowStatus === 'COMPLETED' ? 100 : workflowStatus === 'PENDING' ? 0 : Math.round((activeStep / workflowSteps.length) * 100)} 
                sx={{ mt: 1, height: 6, borderRadius: 3 }}
              />
            </Box>

            <Stack spacing={2}>
              <Button 
                variant="contained" 
                fullWidth 
                startIcon={<PlayArrow />}
                onClick={triggerWorkflow}
                disabled={workflowStatus === 'RUNNING'}
              >
                Start Workflow
              </Button>
              <Button 
                variant="outlined" 
                fullWidth 
                color="error"
                startIcon={<Stop />}
                onClick={cancelWorkflow}
                disabled={workflowStatus !== 'RUNNING'}
              >
                Cancel Execution
              </Button>
            </Stack>
          </Paper>
        </Grid>

        {/* Workflow Timeline map */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Visual Journey Pipeline
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            <Box sx={{ height: 320, overflowY: 'auto', pr: 1 }}>
              <Stepper activeStep={activeStep} orientation="vertical">
                {workflowSteps.map((step, index) => (
                  <Step key={step.name}>
                    <StepLabel
                      optional={
                        <Typography variant="caption" color="text.secondary">
                          {step.desc}
                        </Typography>
                      }
                    >
                      <Typography variant="body2" fontWeight="600">{step.name}</Typography>
                    </StepLabel>
                  </Step>
                ))}
              </Stepper>
            </Box>
          </Paper>
        </Grid>

        {/* Execution logs */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Real-time Underwriting Execution Logs
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            <Box sx={{ maxHeight: 240, overflowY: 'auto', bgcolor: 'rgba(0,0,0,0.2)', p: 2, borderRadius: 1.5, fontFamily: 'monospace', fontSize: '0.85rem' }}>
              {logs.length === 0 ? (
                <Typography variant="body2" color="text.secondary">No active logs. Click "Start Workflow" to execute pipeline.</Typography>
              ) : (
                logs.map((l, idx) => (
                  <Box key={idx} sx={{ display: 'flex', gap: 2, mb: 1 }}>
                    <Typography color="text.secondary">[{l.time}]</Typography>
                    <Typography color={l.status === 'SUCCESS' ? 'success.main' : l.status === 'ERROR' ? 'error.main' : 'primary.main'}>
                      {l.msg}
                    </Typography>
                  </Box>
                ))
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

// Event Engine Dashboard (Reports View)
const EventEnginePage = () => {
  const [isPlaying, setIsPlaying] = React.useState(true);
  const [events, setEvents] = React.useState([
    { id: 'evt_a1b2c3d4', type: 'Customer Registered', time: '17:02:12', target: 'Priya Textile Works', status: 'SUCCESS' },
    { id: 'evt_b2c3d4e5', type: 'GST Return Filed', time: '17:02:15', target: 'Priya Textile Works', status: 'SUCCESS' },
    { id: 'evt_c3d4e5f6', type: 'Financial Health Updated', time: '17:02:16', target: 'Score: 85/100', status: 'SUCCESS' },
    { id: 'evt_d4e5f6g7', type: 'Credit Score Updated', time: '17:02:18', target: 'Credit Score: 780', status: 'SUCCESS' },
    { id: 'evt_e5f6g7h8', type: 'OCEN Offers Generated', time: '17:02:22', target: '4 active offers', status: 'SUCCESS' }
  ]);

  const triggerReplay = () => {
    uiStore.getState().showNotification('Replaying simulation events in queue...', 'info');
  };

  const activeRules = [
    { cond: 'If GST filing delayed > 90 days', action: 'Increase Risk Score', level: 'CRITICAL' },
    { cond: 'If EMI missed twice', action: 'Reduce Credit Score (set 300)', level: 'HIGH' },
    { cond: 'If Revenue grows 20%', action: 'Improve Financial Health metric', level: 'INFO' }
  ];

  return (
    <Box>
      <Typography variant="h5" color="text.primary" fontWeight="bold" sx={{ mb: 1 }}>
        Enterprise Business Event Engine Monitor
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
        Chronological audit trailing, dynamic propagation graphs, and transactional rules execution telemetry.
      </Typography>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <MetricCard title="Total Events Processed" value="12,452" trend="Optimal" icon={<ListAlt />} />
        </Grid>
        <Grid item xs={12} sm={4}>
          <MetricCard title="Propagation Speed" value="0.12 ms" trend="Fast" icon={<Speed />} />
        </Grid>
        <Grid item xs={12} sm={4}>
          <MetricCard title="Active Rules Loaded" value="3 items" trend="Active" icon={<Memory />} />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="subtitle1" fontWeight="bold">Live Event Log Feed</Typography>
              <Stack direction="row" spacing={1}>
                <IconButton size="small" onClick={() => setIsPlaying(!isPlaying)}>
                  {isPlaying ? <Pause /> : <PlayArrow />}
                </IconButton>
                <IconButton size="small" onClick={triggerReplay}>
                  <Refresh />
                </IconButton>
              </Stack>
            </Box>
            <Divider sx={{ mb: 2 }} />

            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Time</TableCell>
                    <TableCell>Event Type</TableCell>
                    <TableCell>Details / Target</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {events.map((evt) => (
                    <TableRow key={evt.id}>
                      <TableCell>{evt.time}</TableCell>
                      <TableCell><Typography variant="body2" fontWeight="600">{evt.type}</Typography></TableCell>
                      <TableCell>{evt.target}</TableCell>
                      <TableCell><StatusBadge status={evt.status} /></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>Active Business Rules Engine</Typography>
            <Divider sx={{ my: 1.5 }} />
            <List>
              {activeRules.map((r, idx) => (
                <ListItem key={idx} disableGutters sx={{ alignItems: 'flex-start', mb: 1.5 }}>
                  <ListItemIcon sx={{ minWidth: 32, mt: 0.5 }}>
                    <CheckCircle color="primary" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={r.cond} 
                    secondary={`Action: ${r.action} | Alert Priority: ${r.level}`}
                    primaryTypographyProps={{ fontSize: '0.875rem', fontWeight: '600' }}
                    secondaryTypographyProps={{ fontSize: '0.75rem' }}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

// Profile Page Component
const ProfilePage = () => {
  const ui = useStore(uiStore);
  const user = ui.user;
  if (!user) return null;

  return (
    <Box>
      <Typography variant="h5" color="text.primary" fontWeight="bold" sx={{ mb: 1 }}>
        User Identity Profile
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
        Secure authentication details and assigned RBAC permission credentials.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 4, textLabel: 'center', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Avatar sx={{ width: 80, height: 80, bgcolor: 'primary.main', mb: 2, fontSize: '2rem' }}>
              {user.full_name[0]}
            </Avatar>
            <Typography variant="h6" fontWeight="bold">{user.full_name}</Typography>
            <Typography variant="body2" color="primary" fontWeight="600" sx={{ mb: 1 }}>{user.role}</Typography>
            <Typography variant="caption" color="text.secondary" sx={{ mb: 3 }}>{user.email || 'No email registered'}</Typography>
            
            <Divider sx={{ width: '100%', my: 2 }} />
            
            <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', gap: 1.5 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2" color="text.secondary">Department</Typography>
                <Typography variant="body2" fontWeight="bold">{user.department}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2" color="text.secondary">Branch Location</Typography>
                <Typography variant="body2" fontWeight="bold">{user.branch}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body2" color="text.secondary">Access Status</Typography>
                <Typography variant="body2" fontWeight="bold" color="success.main">ACTIVE</Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 4, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Assigned Permissions
            </Typography>
            <Divider sx={{ my: 1.5 }} />
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {user.permissions.map((p) => (
                <Chip key={p} label={p.replace('_', ' ')} color="primary" size="small" variant="outlined" />
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

interface PagePlaceholderProps {
  title: string;
}

const PagePlaceholder: React.FC<PagePlaceholderProps> = ({ title }) => (
  <Box>
    <Typography variant="h5" color="text.primary" fontWeight="bold" sx={{ mb: 1 }}>
      {title}
    </Typography>
    <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
      Enterprise Module | Fully Integrated Sandbox.
    </Typography>
    <Paper sx={{ p: 6, textAlign: 'center', border: '1px dashed rgba(255,255,255,0.08)', borderRadius: 2 }}>
      <SmartToy sx={{ fontSize: 48, color: 'primary.main', mb: 2, opacity: 0.8 }} />
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Module Sandbox Activated
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 480, mx: 'auto', mb: 3 }}>
        All API adapters are configured. Click below to synchronize sandbox records.
      </Typography>
      <Button variant="contained" size="large" onClick={() => uiStore.getState().showNotification(`${title} synced successfully.`)}>
        Synchronize Sandbox Data
      </Button>
    </Paper>
  </Box>
);

// ----------------------------------------------------
// 5. MAIN APP DESIGN
// ----------------------------------------------------
export default function App() {
  const ui = useStore(uiStore);

  const demoAccounts = [
    { label: 'Administrator', mobile: '9900112233' },
    { label: 'Executive', mobile: '9834567890' },
    { label: 'Relationship Manager', mobile: '9876543210' },
    { label: 'Trainer', mobile: '9856789012' },
    { label: 'Demo User', mobile: '9988776655' }
  ];

  const [mobile, setMobile] = React.useState('9876543210');
  const [password, setPassword] = React.useState('AarohanPass123!');

  const activeTheme = React.useMemo(() => {
    return createTheme({
      palette: {
        mode: ui.themeMode,
        primary: { main: '#4285F4' },
        secondary: { main: '#34A853' },
        background: {
          default: ui.themeMode === 'dark' ? '#070a13' : '#f8fafd',
          paper: ui.themeMode === 'dark' ? '#0f1628' : '#ffffff'
        },
        text: {
          primary: ui.themeMode === 'dark' ? '#F1F5F9' : '#0f172a',
          secondary: ui.themeMode === 'dark' ? '#94A3B8' : '#475569'
        }
      },
      typography: {
        fontFamily: 'Outfit, Inter, sans-serif',
        h5: { fontWeight: 700 },
        h6: { fontWeight: 600 }
      },
      shape: { borderRadius: 8 }
    });
  }, [ui.themeMode]);

  const navItems = [
    { name: 'Dashboard', icon: <DashboardIcon />, permission: 'dashboard' },
    { name: 'Customer Onboarding', icon: <People />, permission: 'customer_management' },
    { name: 'CKYC', icon: <PersonSearch />, permission: 'ckyc' },
    { name: 'GST Analysis', icon: <Receipt />, permission: 'gst' },
    { name: 'Account Aggregator', icon: <AccountBalance />, permission: 'account_aggregator' },
    { name: 'EPFO', icon: <WorkOutline />, permission: 'epfo' },
    { name: 'MCA', icon: <Business />, permission: 'mca' },
    { name: 'Financial Health Card', icon: <Assessment />, permission: 'financial_health_card' },
    { name: 'AI Credit Engine', icon: <Memory />, permission: 'credit_engine' },
    { name: 'CAM Generator', icon: <Description />, permission: 'cam' },
    { name: 'OCEN Marketplace', icon: <ShoppingCart />, permission: 'ocen' },
    { name: 'RBI Fraud Registry', icon: <Gavel />, permission: 'rbi_fraud' },
    { name: 'Executive Dashboard', icon: <BarChart />, permission: 'reports' },
    { name: 'Enterprise Simulation Engine', icon: <SettingsInputComponent />, permission: 'simulation_engine' },
    { name: 'Reports', icon: <FolderZip />, permission: 'reports' },
    { name: 'Administration', icon: <SupervisorAccount />, permission: 'administration' },
    { name: 'Settings', icon: <SettingsIcon />, permission: 'settings' }
  ];

  const filteredNavItems = React.useMemo(() => {
    if (!ui.user) return [];
    return navItems.filter((item) => ui.user?.permissions.includes(item.permission));
  }, [ui.user]);

  const handleQuickLogin = (m: string) => {
    setMobile(m);
    setPassword('AarohanPass123!');
    ui.login(m, 'AarohanPass123!');
  };

  return (
    <ThemeProvider theme={activeTheme}>
      <CssBaseline />

      {!ui.isAuthenticated ? (
        <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyItems: 'center', bgcolor: 'background.default', py: 6 }}>
          <Container maxWidth="xs">
            <Paper elevation={4} sx={{ p: 4, border: '1px solid rgba(255,255,255,0.06)', borderRadius: 3 }}>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
                <Avatar sx={{ bgcolor: 'primary.main', width: 44, height: 44, mb: 1 }}>
                  <VpnKey />
                </Avatar>
                <Typography variant="h5" fontWeight="bold">
                  Identity Portal Login
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  AAROHAN Digital Underwriting Platform
                </Typography>
              </Box>

              <Stack spacing={2} sx={{ mb: 3 }}>
                <TextField
                  fullWidth
                  label="Registered Mobile Number"
                  value={mobile}
                  onChange={(e) => setMobile(e.target.value)}
                  placeholder="10-digit mobile number"
                />
                <TextField
                  fullWidth
                  type="password"
                  label="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <Button
                  fullWidth
                  size="large"
                  variant="contained"
                  disabled={ui.isLoading}
                  onClick={() => ui.login(mobile, password)}
                >
                  {ui.isLoading ? 'Verifying...' : 'Sign In'}
                </Button>
              </Stack>

              <Divider sx={{ my: 2.5 }}>
                <Typography variant="caption" color="text.secondary">
                  DEMO PITCH QUICK LOGIN
                </Typography>
              </Divider>

              <Grid container spacing={1}>
                {demoAccounts.map((acc) => (
                  <Grid item xs={6} key={acc.label}>
                    <Button
                      fullWidth
                      size="small"
                      variant="outlined"
                      onClick={() => handleQuickLogin(acc.mobile)}
                      sx={{ fontSize: '0.75rem', py: 1 }}
                    >
                      {acc.label}
                    </Button>
                  </Grid>
                ))}
              </Grid>

            </Paper>
          </Container>
        </Box>
      ) : (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
          
          <Drawer
            variant="permanent"
            sx={{
              width: 260,
              flexShrink: 0,
              '& .MuiDrawer-paper': {
                width: 260,
                boxSizing: 'border-box',
                bgcolor: 'background.paper',
                borderRight: '1px solid rgba(255,255,255,0.06)'
              }
            }}
          >
            <Box sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 1.5 }}>
              <Avatar sx={{ bgcolor: 'primary.main', width: 36, height: 36 }}>
                <DashboardIcon />
              </Avatar>
              <Box>
                <Typography variant="subtitle1" fontWeight="bold" color="text.primary">
                  AAROHAN
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Digital twin Sandbox
                </Typography>
              </Box>
            </Box>
            <Divider sx={{ opacity: 0.1 }} />

            <List sx={{ px: 2, py: 2, overflowY: 'auto' }}>
              {filteredNavItems.map((item) => (
                <ListItem key={item.name} disablePadding sx={{ mb: 0.5 }}>
                  <ListItemButton
                    selected={ui.activePage === item.name}
                    onClick={() => ui.setActivePage(item.name)}
                    sx={{
                      borderRadius: 2,
                      '&.Mui-selected': {
                        bgcolor: 'rgba(66, 133, 244, 0.12)',
                        color: 'primary.main',
                        '& .MuiListItemIcon-root': { color: 'primary.main' }
                      }
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: 40, color: 'text.secondary' }}>
                      {item.icon}
                    </ListItemIcon>
                    <ListItemText
                      primary={item.name}
                      primaryTypographyProps={{ fontSize: '0.875rem', fontWeight: ui.activePage === item.name ? '600' : '500' }}
                    />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Drawer>

          <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            
            <AppBar
              position="static"
              color="transparent"
              elevation={0}
              sx={{ borderBottom: '1px solid rgba(255,255,255,0.06)', bgcolor: 'background.paper' }}
            >
              <Toolbar sx={{ justifyContent: 'space-between', px: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {ui.activePage}
                  </Typography>
                  <Chip label={`Profile: ${ui.user?.role}`} color="secondary" size="small" variant="outlined" />
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <IconButton onClick={ui.toggleTheme} color="inherit">
                    {ui.themeMode === 'light' ? <Brightness4 /> : <Brightness7 />}
                  </IconButton>
                  <IconButton color="inherit">
                    <Notifications />
                  </IconButton>
                  <Divider orientation="vertical" flexItem sx={{ mx: 1, opacity: 0.1 }} />
                  
                  <Box 
                    sx={{ display: 'flex', alignItems: 'center', gap: 1, cursor: 'pointer' }}
                    onClick={() => ui.setActivePage('Profile')}
                  >
                    <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main', fontSize: '0.85rem' }}>
                      {ui.user?.full_name[0]}
                    </Avatar>
                    <Typography variant="body2" fontWeight="500" sx={{ display: { xs: 'none', sm: 'block' } }}>
                      {ui.user?.full_name}
                    </Typography>
                  </Box>

                  <IconButton onClick={ui.logout} color="inherit" sx={{ ml: 1 }}>
                    <Logout />
                  </IconButton>
                </Box>
              </Toolbar>
            </AppBar>

            <Box sx={{ flexGrow: 1, p: 4 }}>
              <Container maxWidth="xl" disableGutters>
                {ui.activePage === 'Dashboard' ? (
                  <DashboardPage />
                ) : ui.activePage === 'Profile' ? (
                  <ProfilePage />
                ) : ui.activePage === 'Enterprise Simulation Engine' ? (
                  <SimulationPage />
                ) : ui.activePage === 'Reports' ? (
                  <EventEnginePage />
                ) : ui.activePage === 'Customer Onboarding' ? (
                  <CustomerOnboardingPage />
                ) : ui.activePage === 'CKYC' ? (
                  <CKYCPage />
                ) : ui.activePage === 'GST Analysis' ? (
                  <GSTPage />
                ) : ui.activePage === 'Account Aggregator' ? (
                  <AAPage />
                ) : ui.activePage === 'EPFO' ? (
                  <EPFOPage />
                ) : ui.activePage === 'MCA' ? (
                  <MCAPage />
                ) : ui.activePage === 'CAM Generator' ? (
                  <CAMPage />
                ) : ui.activePage === 'Executive Dashboard' ? (
                  <ExecutiveCommandCenterPage />
                ) : (
                  <PagePlaceholder title={ui.activePage} />
                )}
              </Container>
            </Box>

            <Box sx={{ py: 3, borderTop: '1px solid rgba(255,255,255,0.06)', textAlign: 'center', bgcolor: 'background.paper' }}>
              <Typography variant="caption" color="text.secondary">
                Project AAROHAN Digital Underwriting Platform v1.0.0 (GA) | Powered by Google Cloud
              </Typography>
            </Box>

          </Box>
        </Box>
      )}

      {ui.notification && (
        <Snackbar
          open={ui.notification.open}
          autoHideDuration={4000}
          onClose={ui.closeNotification}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert onClose={ui.closeNotification} severity={ui.notification.severity} sx={{ width: '100%' }}>
            {ui.notification.message}
          </Alert>
        </Snackbar>
      )}

    </ThemeProvider>
  );
}
