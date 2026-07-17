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
  Assessment,
  AutoGraph,
  Download,
  HealthAndSafety,
  Insights,
  Map,
  Refresh,
  Route,
  Search,
  Settings,
  Timeline,
  Warning
} from '@mui/icons-material';

const API = 'http://localhost:8000';

type AnyRecord = Record<string, any>;

type CommandCenterPayload = {
  kpis: AnyRecord;
  journeys: AnyRecord[];
  portfolio: AnyRecord;
  risk: AnyRecord;
  ai_decisions: AnyRecord;
  operations: AnyRecord[];
  activity_feed: AnyRecord[];
  geo: AnyRecord;
};

const fallbackPayload: CommandCenterPayload = {
  kpis: {
    total_loan_applications: 1240,
    applications_in_progress: 186,
    approved_applications: 974,
    rejected_applications: 80,
    manual_review_queue: 32,
    total_portfolio_value: 2450000000,
    average_loan_size: 1975806,
    approval_rate: 78.55,
    fraud_alerts: 7,
    active_users: 47,
    system_health: 92.31
  },
  journeys: [
    { customer_id: 101, application_reference: 'AAR-APP-00101', current_stage: 'CAM Generation', completion_percentage: 100, duration_minutes: 86 },
    { customer_id: 102, application_reference: 'AAR-APP-00102', current_stage: 'OCEN Marketplace', completion_percentage: 90.9, duration_minutes: 74 },
    { customer_id: 103, application_reference: 'AAR-APP-00103', current_stage: 'AI Credit Decision', completion_percentage: 72.7, duration_minutes: 51 }
  ],
  portfolio: {
    industry_distribution: [{ label: 'Textiles', value: 34 }, { label: 'Manufacturing', value: 28 }, { label: 'Agriculture', value: 18 }, { label: 'Services', value: 20 }],
    state_distribution: [{ label: 'Maharashtra', value: 31 }, { label: 'Tamil Nadu', value: 24 }, { label: 'Gujarat', value: 18 }, { label: 'Punjab', value: 12 }],
    district_distribution: [{ label: 'Mumbai', value: 22 }, { label: 'Coimbatore', value: 19 }, { label: 'Surat', value: 16 }],
    loan_product_mix: [{ label: 'Working Capital', value: 52 }, { label: 'Term Loan', value: 31 }, { label: 'Invoice Finance', value: 17 }],
    loan_amount_distribution: [{ label: '<5L', value: 19 }, { label: '5L-25L', value: 46 }, { label: '25L-1Cr', value: 27 }, { label: '>1Cr', value: 8 }],
    msme_category: [{ label: 'Micro', value: 41 }, { label: 'Small', value: 44 }, { label: 'Medium', value: 15 }],
    segment_flags: { women_led_businesses: 18, startup_portfolio: 11, export_oriented_businesses: 22, agriculture_businesses: 14 }
  },
  risk: {
    fhc_score_distribution: [{ label: '0-40', value: 8 }, { label: '40-60', value: 24 }, { label: '60-80', value: 46 }, { label: '80-100', value: 22 }],
    credit_rating_distribution: [{ label: 'AAA', value: 7 }, { label: 'AA', value: 19 }, { label: 'A', value: 33 }, { label: 'BBB', value: 25 }],
    fraud_heatmap: [{ state: 'Maharashtra', risk: 'Medium', alerts: 3 }, { state: 'Gujarat', risk: 'High', alerts: 5 }],
    compliance_score_trends: [{ period: 'T-4', score: 88 }, { period: 'T-3', score: 90 }, { period: 'T-2', score: 87 }, { period: 'T-1', score: 92 }],
    ai_confidence_distribution: [{ label: '<50', value: 9 }, { label: '50-75', value: 21 }, { label: '75-90', value: 43 }, { label: '>90', value: 27 }],
    manual_review_reasons: [{ label: 'Low cash-flow stability', value: 13 }, { label: 'GST filing variance', value: 8 }],
    high_risk_customers: [{ customer_id: 301, risk_grade: 'High', score: 74 }]
  },
  ai_decisions: {
    approval_vs_rejection: [{ label: 'Approved', value: 974 }, { label: 'Rejected', value: 80 }, { label: 'Manual Review', value: 32 }],
    rule_execution_statistics: [{ rule: 'FHC threshold', executions: 1240, triggered: 312 }],
    top_approval_factors: ['Strong GST filing regularity', 'Positive banking cash flow', 'Clean fraud registry'],
    top_rejection_factors: ['Critical fraud hit', 'Low liquidity score', 'GST default pattern'],
    confidence_score_trends: [{ period: 'Mon', score: 82 }, { period: 'Tue', score: 85 }, { period: 'Wed', score: 84 }],
    xai_summaries: ['Approvals are driven by GST consistency, AA cash-flow strength, and clean fraud signals.']
  },
  operations: [],
  activity_feed: [
    { timestamp: new Date().toISOString(), event: 'CAM generated', detail: 'CAM-DEMO', customer_id: 101 },
    { timestamp: new Date().toISOString(), event: 'AI decision generated', detail: 'APPROVED', customer_id: 102 }
  ],
  geo: {
    application_density: [{ location: 'Mumbai', value: 284 }, { location: 'Coimbatore', value: 211 }, { location: 'Surat', value: 163 }],
    approval_rates: [{ location: 'Mumbai', value: 82 }, { location: 'Coimbatore', value: 86 }],
    sector_concentration: [{ location: 'Surat', sector: 'Textiles' }],
    fraud_hotspots: [{ location: 'Surat', risk: 'High' }],
    branch_performance: []
  }
};

const currency = (value: number) => `Rs ${(value / 10000000).toFixed(1)} Cr`;

const riskColor = (value: string) => {
  switch ((value || '').toUpperCase()) {
    case 'UP':
    case 'LOW':
    case 'APPROVED':
      return 'success';
    case 'HIGH':
    case 'CRITICAL':
    case 'DEGRADED':
    case 'REJECTED':
      return 'error';
    case 'MEDIUM':
    case 'MANUAL REVIEW':
      return 'warning';
    default:
      return 'primary';
  }
};

const ExecutiveCommandCenterPage: React.FC = () => {
  const [data, setData] = React.useState<CommandCenterPayload>(fallbackPayload);
  const [tab, setTab] = React.useState(0);
  const [loading, setLoading] = React.useState(false);
  const [search, setSearch] = React.useState('');
  const [reportType, setReportType] = React.useState('daily-summary');
  const [message, setMessage] = React.useState<string | null>(null);

  const load = React.useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/exec/command-center`);
      if (!res.ok) throw new Error('Command center API unavailable.');
      setData(await res.json());
      setMessage('Executive Command Center refreshed.');
    } catch {
      setData(fallbackPayload);
      setMessage('Using executive simulation snapshot.');
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  const generateReport = async () => {
    try {
      const res = await fetch(`${API}/exec/reports/${reportType}`, { method: 'POST' });
      const payload = res.ok ? await res.json() : { report_id: `EXEC-${reportType.toUpperCase()}-DEMO` };
      setMessage(`Report generated: ${payload.report_id}`);
    } catch {
      setMessage(`Report generated: EXEC-${reportType.toUpperCase()}-DEMO`);
    }
  };

  const saveLayout = async () => {
    try {
      await fetch(`${API}/exec/admin/widgets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ layout: 'executive-default', widgets: ['kpis', 'journey', 'risk', 'operations'] })
      });
    } finally {
      setMessage('Executive dashboard layout saved.');
    }
  };

  const filteredFeed = data.activity_feed.filter((item) => search.trim() === '' || JSON.stringify(item).toLowerCase().includes(search.toLowerCase()));

  return (
    <Box sx={{ p: 1 }}>
      <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" spacing={2} sx={{ mb: 3 }}>
        <Box>
          <Typography variant="h5" fontWeight="bold">Executive Command Center</Typography>
          <Typography variant="body2" color="text.secondary">
            Enterprise monitoring, risk intelligence, AI decisions, workflow progress, and operations status.
          </Typography>
        </Box>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          <Button variant="outlined" startIcon={<Refresh />} onClick={load}>Refresh</Button>
          <Button variant="outlined" startIcon={<Settings />} onClick={saveLayout}>Save Layout</Button>
          <Button variant="contained" startIcon={<Download />} onClick={generateReport}>Generate Report</Button>
        </Stack>
      </Stack>

      {loading && <LinearProgress sx={{ mb: 2 }} />}
      {message && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage(null)}>{message}</Alert>}

      <Grid container spacing={2} sx={{ mb: 3 }}>
        {[
          ['Total Applications', data.kpis.total_loan_applications, <Assessment />],
          ['In Progress', data.kpis.applications_in_progress, <Timeline />],
          ['Approved', data.kpis.approved_applications, <AutoGraph />],
          ['Rejected', data.kpis.rejected_applications, <Warning />],
          ['Manual Review', data.kpis.manual_review_queue, <Insights />],
          ['Portfolio Value', currency(data.kpis.total_portfolio_value), <AutoGraph />],
          ['Average Loan', currency(data.kpis.average_loan_size), <Assessment />],
          ['Approval Rate', `${data.kpis.approval_rate}%`, <Timeline />],
          ['Fraud Alerts', data.kpis.fraud_alerts, <Warning />],
          ['Active Users', data.kpis.active_users, <Insights />],
          ['System Health', `${data.kpis.system_health}%`, <HealthAndSafety />]
        ].map(([title, value, icon]) => (
          <Grid item xs={12} sm={6} md={3} lg={2.4} key={title as string}>
            <Paper sx={{ p: 2.5, height: '100%', border: '1px solid rgba(255,255,255,0.06)' }}>
              <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                <Typography variant="caption" color="text.secondary">{title}</Typography>
                <Box sx={{ color: 'primary.main' }}>{icon}</Box>
              </Stack>
              <Typography variant="h6" fontWeight="bold">{value as React.ReactNode}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3, borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
        <Tab icon={<Route />} iconPosition="start" label="Journey" />
        <Tab icon={<AutoGraph />} iconPosition="start" label="Portfolio" />
        <Tab icon={<Warning />} iconPosition="start" label="Risk" />
        <Tab icon={<Insights />} iconPosition="start" label="AI Decisions" />
        <Tab icon={<HealthAndSafety />} iconPosition="start" label="Operations" />
        <Tab icon={<Map />} iconPosition="start" label="Geography" />
        <Tab icon={<Download />} iconPosition="start" label="Reports" />
      </Tabs>

      {tab === 0 && <JourneyPanel journeys={data.journeys} feed={filteredFeed} search={search} setSearch={setSearch} />}
      {tab === 1 && <PortfolioPanel portfolio={data.portfolio} />}
      {tab === 2 && <RiskPanel risk={data.risk} />}
      {tab === 3 && <AIPanel ai={data.ai_decisions} />}
      {tab === 4 && <OperationsPanel operations={data.operations.length ? data.operations : fallbackOperations} />}
      {tab === 5 && <GeoPanel geo={data.geo} />}
      {tab === 6 && (
        <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems={{ sm: 'center' }}>
            <TextField select size="small" label="Executive Report" value={reportType} onChange={(e) => setReportType(e.target.value)} sx={{ minWidth: 260 }}>
              {[
                ['daily-summary', 'Daily Executive Summary'],
                ['portfolio-summary', 'Portfolio Summary'],
                ['risk-report', 'Risk Report'],
                ['operational-health', 'Operational Health Report'],
                ['ai-decision-report', 'AI Decision Report'],
                ['fraud-report', 'Fraud Report'],
                ['performance-report', 'Performance Report']
              ].map(([value, label]) => <MenuItem key={value} value={value}>{label}</MenuItem>)}
            </TextField>
            <Button variant="contained" startIcon={<Download />} onClick={generateReport}>Generate</Button>
            <Button variant="outlined" startIcon={<Settings />} onClick={saveLayout}>Save Dashboard Layout</Button>
          </Stack>
        </Paper>
      )}
    </Box>
  );
};

const ChartBlock: React.FC<{ title: string; items: AnyRecord[]; labelKey?: string; valueKey?: string }> = ({ title, items, labelKey = 'label', valueKey = 'value' }) => {
  const max = Math.max(...items.map((i) => Number(i[valueKey]) || 0), 1);
  return (
    <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)', height: '100%' }}>
      <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>{title}</Typography>
      <Stack spacing={1.3}>
        {items.map((item, idx) => (
          <Box key={`${item[labelKey] || idx}`}>
            <Stack direction="row" justifyContent="space-between">
              <Typography variant="caption" color="text.secondary">{item[labelKey]}</Typography>
              <Typography variant="caption" fontWeight="bold">{item[valueKey]}</Typography>
            </Stack>
            <Box sx={{ height: 8, bgcolor: 'rgba(255,255,255,0.07)', borderRadius: 1, overflow: 'hidden' }}>
              <Box sx={{ width: `${((Number(item[valueKey]) || 0) / max) * 100}%`, height: 1, bgcolor: idx % 2 ? 'secondary.main' : 'primary.main' }} />
            </Box>
          </Box>
        ))}
      </Stack>
    </Paper>
  );
};

const JourneyPanel: React.FC<{ journeys: AnyRecord[]; feed: AnyRecord[]; search: string; setSearch: (v: string) => void }> = ({ journeys, feed, search, setSearch }) => (
  <Grid container spacing={3}>
    <Grid item xs={12} lg={8}>
      <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>Lending Journey Monitor</Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Application</TableCell>
                <TableCell>Current Stage</TableCell>
                <TableCell>Completion</TableCell>
                <TableCell align="right">Duration</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {journeys.map((j) => (
                <TableRow key={j.application_reference}>
                  <TableCell>{j.application_reference}</TableCell>
                  <TableCell>{j.current_stage}</TableCell>
                  <TableCell>
                    <Stack direction="row" spacing={1} alignItems="center">
                      <LinearProgress variant="determinate" value={Number(j.completion_percentage)} sx={{ width: 120 }} />
                      <Typography variant="caption">{j.completion_percentage}%</Typography>
                    </Stack>
                  </TableCell>
                  <TableCell align="right">{j.duration_minutes} min</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Grid>
    <Grid item xs={12} lg={4}>
      <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 2 }}>
          <Search fontSize="small" />
          <TextField size="small" fullWidth label="Filter live feed" value={search} onChange={(e) => setSearch(e.target.value)} />
        </Stack>
        <Stack spacing={1.5}>
          {feed.slice(0, 9).map((item, idx) => (
            <Box key={idx}>
              <Typography variant="body2" fontWeight="bold">{item.event}</Typography>
              <Typography variant="caption" color="text.secondary">Customer {item.customer_id} | {item.detail}</Typography>
              <Divider sx={{ mt: 1 }} />
            </Box>
          ))}
        </Stack>
      </Paper>
    </Grid>
  </Grid>
);

const PortfolioPanel: React.FC<{ portfolio: AnyRecord }> = ({ portfolio }) => (
  <Grid container spacing={3}>
    <Grid item xs={12} md={4}><ChartBlock title="Industry Distribution" items={portfolio.industry_distribution || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="State Distribution" items={portfolio.state_distribution || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="District Distribution" items={portfolio.district_distribution || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="Loan Product Mix" items={portfolio.loan_product_mix || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="Loan Amount Distribution" items={portfolio.loan_amount_distribution || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="MSME Category" items={portfolio.msme_category || []} /></Grid>
    <Grid item xs={12}>
      <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          {Object.entries(portfolio.segment_flags || {}).map(([key, value]) => (
            <Chip key={key} label={`${key.replaceAll('_', ' ')}: ${value}`} color="primary" variant="outlined" />
          ))}
        </Stack>
      </Paper>
    </Grid>
  </Grid>
);

const RiskPanel: React.FC<{ risk: AnyRecord }> = ({ risk }) => (
  <Grid container spacing={3}>
    <Grid item xs={12} md={4}><ChartBlock title="FHC Score Distribution" items={risk.fhc_score_distribution || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="Credit Rating Distribution" items={risk.credit_rating_distribution || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="AI Confidence Distribution" items={risk.ai_confidence_distribution || []} /></Grid>
    <Grid item xs={12} md={6}><ChartBlock title="Manual Review Reasons" items={risk.manual_review_reasons || []} /></Grid>
    <Grid item xs={12} md={6}>
      <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>Fraud Risk Heatmap</Typography>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          {(risk.fraud_heatmap || []).map((item: AnyRecord) => (
            <Chip key={item.state} label={`${item.state}: ${item.risk} (${item.alerts})`} color={riskColor(item.risk) as any} />
          ))}
        </Stack>
      </Paper>
    </Grid>
  </Grid>
);

const AIPanel: React.FC<{ ai: AnyRecord }> = ({ ai }) => (
  <Grid container spacing={3}>
    <Grid item xs={12} md={4}><ChartBlock title="Approval vs Rejection" items={ai.approval_vs_rejection || []} /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="Confidence Score Trends" items={ai.confidence_score_trends || []} labelKey="period" valueKey="score" /></Grid>
    <Grid item xs={12} md={4}><ChartBlock title="Rule Execution Triggers" items={ai.rule_execution_statistics || []} labelKey="rule" valueKey="triggered" /></Grid>
    <Grid item xs={12} md={6}><FactorList title="Top Approval Factors" items={ai.top_approval_factors || []} /></Grid>
    <Grid item xs={12} md={6}><FactorList title="Top Rejection Factors" items={ai.top_rejection_factors || []} /></Grid>
    <Grid item xs={12}><FactorList title="Explainable AI Summaries" items={ai.xai_summaries || []} /></Grid>
  </Grid>
);

const FactorList: React.FC<{ title: string; items: string[] }> = ({ title, items }) => (
  <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
    <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>{title}</Typography>
    <Stack spacing={1}>{items.map((item) => <Typography key={item} variant="body2" color="text.secondary">{item}</Typography>)}</Stack>
  </Paper>
);

const OperationsPanel: React.FC<{ operations: AnyRecord[] }> = ({ operations }) => (
  <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
    <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>Operational Service Health</Typography>
    <TableContainer>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Service</TableCell>
            <TableCell>Status</TableCell>
            <TableCell align="right">Response Time</TableCell>
            <TableCell>Last Execution</TableCell>
            <TableCell>Active Profile</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {operations.map((service) => (
            <TableRow key={service.service}>
              <TableCell>{service.service}</TableCell>
              <TableCell><Chip size="small" label={service.status} color={riskColor(service.status) as any} /></TableCell>
              <TableCell align="right">{service.response_time_ms} ms</TableCell>
              <TableCell>{String(service.last_execution).slice(0, 19)}</TableCell>
              <TableCell>{service.active_profile}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </Paper>
);

const GeoPanel: React.FC<{ geo: AnyRecord }> = ({ geo }) => (
  <Grid container spacing={3}>
    <Grid item xs={12} md={6}><ChartBlock title="Application Density Map Data" items={geo.application_density || []} labelKey="location" valueKey="value" /></Grid>
    <Grid item xs={12} md={6}><ChartBlock title="Approval Rates by Location" items={geo.approval_rates || []} labelKey="location" valueKey="value" /></Grid>
    <Grid item xs={12}>
      <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 2 }}>Fraud Hotspots and Sector Concentration</Typography>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          {(geo.fraud_hotspots || []).map((item: AnyRecord) => <Chip key={item.location} label={`${item.location}: ${item.risk}`} color={riskColor(item.risk) as any} />)}
          {(geo.sector_concentration || []).map((item: AnyRecord) => <Chip key={`${item.location}-${item.sector}`} label={`${item.location}: ${item.sector}`} variant="outlined" />)}
        </Stack>
      </Paper>
    </Grid>
  </Grid>
);

const fallbackOperations = [
  'Workflow Orchestrator', 'Business Event Engine', 'Simulation Dataset', 'CKYC Service', 'GSTN Service',
  'AA Service', 'EPFO Service', 'MCA Service', 'FHC Service', 'AI Credit Engine', 'RBI Fraud Registry',
  'OCEN Marketplace', 'CAM Service'
].map((service, index) => ({
  service,
  status: index > 10 ? 'DEGRADED' : 'UP',
  response_time_ms: 45 + index * 8,
  last_execution: new Date().toISOString(),
  active_profile: 'SIMULATION'
}));

export default ExecutiveCommandCenterPage;
