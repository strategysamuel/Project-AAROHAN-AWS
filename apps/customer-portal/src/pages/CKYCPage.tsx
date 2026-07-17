import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Grid, Paper, TextField, Button, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Chip, CircularProgress,
  Alert, Card, CardContent, Divider, Dialog, DialogTitle, DialogContent,
  DialogActions, Stack, Avatar, LinearProgress, Tab, Tabs
} from '@mui/material';
import {
  Search, Shield, Security, Warning, CheckCircle, Refresh,
  Cancel, HelpOutline, AssignmentInd, AdminPanelSettings, Download
} from '@mui/icons-material';
import { apiUrl } from '../lib/api';

interface CKYCRecord {
  id: number;
  customer_id: number;
  ckyc_number: string;
  full_name: string;
  dob: string;
  pan: string;
  aadhaar_masked?: string;
  address?: string;
  mobile?: string;
  email?: string;
  kyc_status: string;
  last_synced_at: string;
}

interface VerificationLog {
  id: number;
  customer_id: number;
  checked_by: string;
  match_confidence: number;
  risk_indicators: string;
  anomaly_detected: boolean;
  verification_status: string;
  comments?: string;
  verified_at: string;
}

const API = apiUrl(''); // Auth/onboarding gateway or local ports

const CKYCPage: React.FC = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [panQuery, setPanQuery] = useState('ABCDE1234F');
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchResult, setSearchResult] = useState<CKYCRecord | null>(null);
  const [verificationLog, setVerificationLog] = useState<VerificationLog | null>(null);
  
  // Admin & History States
  const [logs, setLogs] = useState<VerificationLog[]>([]);
  const [manualQueue, setManualQueue] = useState<VerificationLog[]>([]);
  const [stats, setStats] = useState<Record<string, number>>({
    VERIFIED: 0, VERIFIED_WITH_WARNING: 0, PENDING: 0,
    MANUAL_REVIEW: 0, FAILED: 0, TOTAL: 0
  });
  
  // Dialog State
  const [overrideDialogOpen, setOverrideDialogOpen] = useState(false);
  const [selectedLogId, setSelectedLogId] = useState<number | null>(null);
  const [overrideStatus, setOverrideStatus] = useState('VERIFIED');
  const [overrideComments, setOverrideComments] = useState('');
  const [adminCheckedBy, setAdminCheckedBy] = useState('ADMIN-SYSTEM-99');
  
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Fetch stats and history on mount
  useEffect(() => {
    fetchStats();
    fetchLogs();
    fetchManualQueue();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API}/ckyc/stats`);
      if (!res.ok) throw new Error(); setStats(await res.json());
    } catch {
      // Mock stats for demo mode
      setStats({
        VERIFIED: 12, VERIFIED_WITH_WARNING: 3, PENDING: 1,
        MANUAL_REVIEW: 2, FAILED: 1, TOTAL: 19
      });
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await fetch(`${API}/ckyc/verification-logs`);
      if (!res.ok) throw new Error(); setLogs(await res.json());
    } catch {
      // Mock log history
      setLogs([
        {
          id: 1, customer_id: 125, checked_by: 'SYSTEM', match_confidence: 100.0,
          risk_indicators: '', anomaly_detected: false, verification_status: 'VERIFIED',
          verified_at: new Date().toISOString()
        }
      ]);
    }
  };

  const fetchManualQueue = async () => {
    try {
      const res = await fetch(`${API}/ckyc/manual-queue`);
      if (!res.ok) throw new Error(); setManualQueue(await res.json());
    } catch {
      setManualQueue([
        {
          id: 2, customer_id: 126, checked_by: 'SYSTEM', match_confidence: 65.0,
          risk_indicators: 'Name Mismatch,Address Mismatch', anomaly_detected: true,
          verification_status: 'MANUAL REVIEW', verified_at: new Date().toISOString()
        }
      ]);
    }
  };

  const handleSearch = async () => {
    setSearchLoading(true);
    setError(null);
    setSearchResult(null);
    setVerificationLog(null);

    try {
      const res = await fetch(`${API}/ckyc/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pan: panQuery })
      });
      if (res.ok) {
        const record = await res.json();
        setSearchResult(record);
        
        // Auto-fetch verification details
        const verifyRes = await fetch(`${API}/ckyc/verify/${record.customer_id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ checked_by: 'RM-SYSTEM-CONSOLE' })
        });
        if (verifyRes.ok) {
          setVerificationLog(await verifyRes.json());
        }
      } else { throw new Error(); }
    } catch {
      // Mock Fallback
      setSearchResult({
        id: 1, customer_id: 125, ckyc_number: '30049281726354',
        full_name: 'Aditya Patel', dob: '12-08-1988', pan: panQuery,
        aadhaar_masked: 'XXXXXXXX9876', address: 'Plot 42, MIDC, Mumbai, Maharashtra - 400001',
        mobile: '9876543210', email: 'aditya@garments.com', kyc_status: 'VERIFIED',
        last_synced_at: new Date().toISOString()
      });
      setVerificationLog({
        id: 1, customer_id: 125, checked_by: 'SYSTEM', match_confidence: 100.0,
        risk_indicators: '', anomaly_detected: false, verification_status: 'VERIFIED',
        verified_at: new Date().toISOString()
      });
    } finally {
      setSearchLoading(false);
      fetchStats();
      fetchLogs();
    }
  };

  const handleReRun = async (customerId: number) => {
    setSearchLoading(true);
    try {
      const res = await fetch(`${API}/ckyc/verify/${customerId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ checked_by: 'RM-MANUAL-RERUN' })
      });
      if (res.ok) {
        setVerificationLog(await res.json());
        setSuccess('✓ Verification re-run completed successfully!');
        fetchLogs();
      }
    } catch {
      setSuccess('✓ Verification re-run completed (mock demo mode).');
    } finally {
      setSearchLoading(false);
    }
  };

  const openOverrideDialog = (logId: number) => {
    setSelectedLogId(logId);
    setOverrideStatus('VERIFIED');
    setOverrideComments('');
    setOverrideDialogOpen(true);
  };

  const handleOverrideSubmit = async () => {
    if (!selectedLogId) return;
    try {
      const res = await fetch(`${API}/ckyc/override/${selectedLogId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          checked_by: adminCheckedBy,
          status: overrideStatus,
          comments: overrideComments
        })
      });
      if (res.ok) {
        setSuccess('✓ CKYC status overridden successfully.');
        fetchLogs();
        fetchManualQueue();
        fetchStats();
      }
    } catch {
      setSuccess('✓ CKYC status overridden (mock mode).');
    } finally {
      setOverrideDialogOpen(false);
    }
  };

  const handleExport = () => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + ["Log ID,Customer ID,Verification Status,Match Confidence %,Risks,Checked By,Date"].join(",") + "\n"
      + logs.map(l => [l.id, l.customer_id, l.verification_status, l.match_confidence, l.risk_indicators.replace(/,/g, "|"), l.checked_by, l.verified_at].join(",")).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `CKYC_Report_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getStatusColor = (status: string) => {
    switch (status?.toUpperCase()) {
      case 'VERIFIED': return 'success';
      case 'VERIFIED WITH WARNING':
      case 'VERIFIED_WITH_WARNING': return 'info';
      case 'MANUAL REVIEW':
      case 'MANUAL_REVIEW': return 'warning';
      case 'FAILED':
      case 'DATA MISMATCH':
      case 'DUPLICATE RECORD': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 1 }}>
      {/* CKYC Stats Dashboard */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {Object.entries(stats).map(([key, val]) => (
          key !== 'TOTAL' && (
            <Grid item xs={6} sm={3} md={1.7} key={key}>
              <Card sx={{ bgcolor: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)' }}>
                <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                  <Typography variant="caption" color="text.secondary" noWrap sx={{ display: 'block' }}>
                    {key.replace(/_/g, ' ')}
                  </Typography>
                  <Typography variant="h5" fontWeight="bold" sx={{ mt: 0.5 }}>
                    {val}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          )
        ))}
        <Grid item xs={12} sm={3} md={1.8}>
          <Card sx={{ bgcolor: 'rgba(66,133,244,0.05)', border: '1px solid rgba(66,133,244,0.2)' }}>
            <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
              <Typography variant="caption" color="primary.main" fontWeight="bold">TOTAL RECORDS</Typography>
              <Typography variant="h5" fontWeight="bold" color="primary.main" sx={{ mt: 0.5 }}>
                {stats.TOTAL}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Tabs value={tabIndex} onChange={(_, idx) => setTabIndex(idx)} sx={{ mb: 3, borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <Tab label="Verification Console" icon={<AssignmentInd />} iconPosition="start" />
        <Tab label="Manual Review Queue" icon={<AdminPanelSettings />} iconPosition="start" />
        <Tab label="Audit Log History" icon={<Security />} iconPosition="start" />
      </Tabs>

      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>{success}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {/* Verification Console */}
      {tabIndex === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={5}>
            <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
              <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>CKYC Registry Search</Typography>
              <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
                <TextField
                  fullWidth
                  size="small"
                  label="Search by PAN"
                  value={panQuery}
                  onChange={e => setPanQuery(e.target.value.toUpperCase())}
                  placeholder="AAAAA9999A"
                />
                <Button variant="contained" onClick={handleSearch} disabled={searchLoading} startIcon={<Search />}>
                  Search
                </Button>
              </Box>

              {searchLoading && <LinearProgress sx={{ my: 2 }} />}

              {searchResult && (
                <Stack spacing={2.5}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar sx={{ bgcolor: 'primary.main', width: 44, height: 44 }}>
                      {searchResult.full_name[0]}
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle2" fontWeight="bold">{searchResult.full_name}</Typography>
                      <Typography variant="caption" color="text.secondary">CKYC Identifier: {searchResult.ckyc_number}</Typography>
                    </Box>
                  </Box>
                  
                  <Divider />

                  <Grid container spacing={1.5} sx={{ fontSize: '0.85rem' }}>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">PAN</Typography>
                      <Typography variant="body2" fontWeight="500">{searchResult.pan}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">Aadhaar (Demo)</Typography>
                      <Typography variant="body2" fontWeight="500">{searchResult.aadhaar_masked || '–'}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">Date of Birth</Typography>
                      <Typography variant="body2" fontWeight="500">{searchResult.dob}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">Mobile</Typography>
                      <Typography variant="body2" fontWeight="500">{searchResult.mobile || '–'}</Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="caption" color="text.secondary">Address</Typography>
                      <Typography variant="body2" fontWeight="500">{searchResult.address || '–'}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">Registry Status</Typography>
                      <Box sx={{ mt: 0.5 }}>
                        <Chip label={searchResult.kyc_status} color={getStatusColor(searchResult.kyc_status)} size="small" />
                      </Box>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">Last Sync Time</Typography>
                      <Typography variant="body2" fontWeight="500">{new Date(searchResult.last_synced_at).toLocaleString()}</Typography>
                    </Grid>
                  </Grid>

                  <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                    <Button fullWidth size="small" variant="outlined" startIcon={<Refresh />} onClick={() => handleReRun(searchResult.customer_id)}>
                      Re-run Verification
                    </Button>
                  </Box>
                </Stack>
              )}
            </Paper>
          </Grid>

          {/* Results Widget */}
          <Grid item xs={12} md={7}>
            {verificationLog ? (
              <Paper sx={{ p: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="subtitle1" fontWeight="bold">Identity Match Appraisal</Typography>
                  <Chip
                    icon={verificationLog.anomaly_detected ? <Warning /> : <CheckCircle />}
                    label={verificationLog.verification_status}
                    color={getStatusColor(verificationLog.verification_status)}
                  />
                </Box>
                
                <Divider sx={{ my: 2 }} />

                {/* Score Widget */}
                <Box sx={{ py: 2, textAlign: 'center' }}>
                  <Typography variant="caption" color="text.secondary">Identity Confidence Score</Typography>
                  <Typography variant="h3" color={verificationLog.match_confidence >= 80 ? 'success.main' : verificationLog.match_confidence >= 50 ? 'warning.main' : 'error.main'} fontWeight="bold" sx={{ my: 1 }}>
                    {verificationLog.match_confidence}%
                  </Typography>
                  <Box sx={{ width: '80%', mx: 'auto' }}>
                    <LinearProgress
                      variant="determinate"
                      value={verificationLog.match_confidence}
                      color={verificationLog.match_confidence >= 80 ? 'success' : verificationLog.match_confidence >= 50 ? 'warning' : 'error'}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                </Box>

                <Divider sx={{ my: 2 }} />

                {/* Risk Indicators */}
                <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 1.5 }}>Risk Indicator Analysis</Typography>
                <Stack spacing={1}>
                  {verificationLog.risk_indicators ? (
                    verificationLog.risk_indicators.split(',').map(r => (
                      <Alert key={r} severity={r.includes('Invalid') || r.includes('Duplicate') ? 'error' : 'warning'} icon={<Warning fontSize="small" />} sx={{ py: 0.5 }}>
                        <strong>{r}</strong>: Flagged anomaly during comparative registry check.
                      </Alert>
                    ))
                  ) : (
                    <Alert severity="success" icon={<CheckCircle fontSize="small" />}>
                      No risk indicators detected. Customer profile matches registry fields perfectly.
                    </Alert>
                  )}
                </Stack>

                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="caption" color="text.secondary">
                    Verified By: <strong>{verificationLog.checked_by}</strong> · {new Date(verificationLog.verified_at).toLocaleString()}
                  </Typography>
                  {verificationLog.verification_status === 'MANUAL REVIEW' && (
                    <Button variant="outlined" color="primary" size="small" onClick={() => openOverrideDialog(verificationLog.id)}>
                      Approve/Override Status
                    </Button>
                  )}
                </Box>
              </Paper>
            ) : (
              <Paper sx={{ p: 6, textAlign: 'center', border: '1px dashed rgba(255,255,255,0.08)' }}>
                <Shield sx={{ fontSize: 48, opacity: 0.4, mb: 1 }} />
                <Typography variant="subtitle2" color="text.secondary">
                  Search a customer above to generate risk analysis and matching confidence metrics.
                </Typography>
              </Paper>
            )}
          </Grid>
        </Grid>
      )}

      {/* Manual Review Queue */}
      {tabIndex === 1 && (
        <TableContainer component={Paper} sx={{ border: '1px solid rgba(255,255,255,0.06)' }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Log ID</strong></TableCell>
                <TableCell><strong>Customer ID</strong></TableCell>
                <TableCell><strong>Confidence Score</strong></TableCell>
                <TableCell><strong>Identified Risks</strong></TableCell>
                <TableCell><strong>Triggered Date</strong></TableCell>
                <TableCell><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {manualQueue.map(q => (
                <TableRow key={q.id}>
                  <TableCell>{q.id}</TableCell>
                  <TableCell>{q.customer_id}</TableCell>
                  <TableCell><Typography color="warning.main" fontWeight="bold">{q.match_confidence}%</Typography></TableCell>
                  <TableCell>
                    {q.risk_indicators.split(',').map(r => (
                      <Chip key={r} label={r} size="small" color="warning" sx={{ m: 0.5 }} />
                    ))}
                  </TableCell>
                  <TableCell>{new Date(q.verified_at).toLocaleDateString()}</TableCell>
                  <TableCell>
                    <Button size="small" variant="contained" color="primary" onClick={() => openOverrideDialog(q.id)}>
                      Approve/Reject
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
              {manualQueue.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <Typography variant="body2" color="text.secondary" sx={{ py: 3 }}>
                      ✓ Manual review queue is completely empty.
                    </Typography>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Audit Log History */}
      {tabIndex === 2 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button variant="outlined" startIcon={<Download />} onClick={handleExport}>
              Export CKYC Report
            </Button>
          </Box>
          <TableContainer component={Paper} sx={{ border: '1px solid rgba(255,255,255,0.06)' }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell><strong>Log ID</strong></TableCell>
                  <TableCell><strong>Customer ID</strong></TableCell>
                  <TableCell><strong>Verification Status</strong></TableCell>
                  <TableCell><strong>Confidence Score</strong></TableCell>
                  <TableCell><strong>Risk Indicators</strong></TableCell>
                  <TableCell><strong>Checked By</strong></TableCell>
                  <TableCell><strong>Date Verified</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {logs.map(l => (
                  <TableRow key={l.id}>
                    <TableCell>{l.id}</TableCell>
                    <TableCell>{l.customer_id}</TableCell>
                    <TableCell>
                      <Chip label={l.verification_status} color={getStatusColor(l.verification_status)} size="small" />
                    </TableCell>
                    <TableCell>{l.match_confidence}%</TableCell>
                    <TableCell>{l.risk_indicators || 'None'}</TableCell>
                    <TableCell>{l.checked_by}</TableCell>
                    <TableCell>{new Date(l.verified_at).toLocaleString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      {/* Admin Override Dialog */}
      <Dialog open={overrideDialogOpen} onClose={() => setOverrideDialogOpen(false)}>
        <DialogTitle>Administrator Identity Verification Override</DialogTitle>
        <DialogContent sx={{ minWidth: 420 }}>
          <Stack spacing={2} sx={{ mt: 1.5 }}>
            <Alert severity="warning">
              This action overrides the automated risk scoring pipeline. All overrides are permanently recorded in the audit trail.
            </Alert>
            <TextField
              select
              label="Override Outcome Status"
              value={overrideStatus}
              onChange={e => setOverrideStatus(e.target.value)}
              SelectProps={{ native: true }}
              fullWidth
            >
              <option value="VERIFIED">VERIFIED</option>
              <option value="VERIFIED WITH WARNING">VERIFIED WITH WARNING</option>
              <option value="FAILED">FAILED</option>
              <option value="DATA MISMATCH">DATA MISMATCH</option>
            </TextField>
            <TextField
              label="Admin Identity Code / Sign-off"
              value={adminCheckedBy}
              onChange={e => setAdminCheckedBy(e.target.value)}
              fullWidth
            />
            <TextField
              label="Audit Comments / Justification"
              value={overrideComments}
              onChange={e => setOverrideComments(e.target.value)}
              multiline
              rows={3}
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOverrideDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleOverrideSubmit}>Submit Sign-off Override</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CKYCPage;
