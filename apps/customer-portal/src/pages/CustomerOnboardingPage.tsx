import React, { useState } from 'react';
import {
  Box, Stepper, Step, StepLabel, StepContent, Button, Typography,
  TextField, MenuItem, Grid, Chip, Alert, Card, CardContent,
  Table, TableBody, TableCell, TableHead, TableRow, LinearProgress,
  Divider, Paper, Avatar, IconButton, Tooltip
} from '@mui/material';
import {
  Person, Business, UploadFile, PlayArrow, CheckCircle,
  Warning, Info, Refresh, Search, Add, ArrowBack, ArrowForward
} from '@mui/icons-material';
import { apiUrl } from '../lib/api';

// ── Types ────────────────────────────────────────────────────────────────────

interface CustomerForm {
  legal_name: string;
  pan: string;
  aadhaar_masked: string;
  mobile_number: string;
  email: string;
  district: string;
  persona_name: string;
  onboarding_status: string;
  address_line1: string;
  state: string;
  pincode: string;
}

interface BusinessForm {
  trade_name: string;
  gstin: string;
  udyam_number: string;
  cin: string;
  constitution_type: string;
  annual_turnover: string;
  industry_segment: string;
  business_vintage_years: string;
  employee_count: string;
  existing_banking: string;
}

interface UploadedDoc {
  doc_type: string;
  doc_name: string;
  source: string;
  status: string;
}

interface ValidationResult { field: string; valid: boolean; message: string; }

// ── Constants ─────────────────────────────────────────────────────────────────

const PERSONAS = ['Priya Textile Works', 'GreenAgro Cooperative', 'QuickLogistics Services'];
const PERSONA_FALLBACKS: Record<string, { customer: Partial<CustomerForm>; business: Partial<BusinessForm> }> = {
  'Priya Textile Works': {
    customer: {
      legal_name: 'Priya Textile Works',
      mobile_number: '9876543210',
      email: 'priya@textileworks.in',
      pan: 'PRXPT0001K',
      aadhaar_masked: 'XXXXXXXX1234',
      district: 'Surat',
    },
    business: {
      trade_name: 'Priya Textile Works Pvt Ltd',
      gstin: '27SIMPT0001K1Z5',
      udyam_number: 'UDYAM-GJ-05-0023456',
      constitution_type: 'Private Limited',
      annual_turnover: '45000000',
      industry_segment: 'Manufacturing – Textiles',
      business_vintage_years: '12',
      employee_count: '87',
      existing_banking: 'SBI, HDFC Bank'
    }
  },
  'GreenAgro Cooperative': {
    customer: {
      legal_name: 'GreenAgro Cooperative Society',
      mobile_number: '9834567890',
      email: 'admin@greenagro.coop',
      pan: 'GRNAG0002B',
      aadhaar_masked: 'XXXXXXXX5678',
      district: 'Nashik',
    },
    business: {
      trade_name: 'GreenAgro Cooperative Society',
      gstin: '27SIMGA0002B1Z8',
      udyam_number: 'UDYAM-MH-11-0087654',
      constitution_type: 'Cooperative',
      annual_turnover: '28000000',
      industry_segment: 'Agriculture',
      business_vintage_years: '8',
      employee_count: '34',
      existing_banking: 'Bank of Maharashtra'
    }
  },
  'QuickLogistics Services': {
    customer: {
      legal_name: 'Quick Logistics Services Pvt Ltd',
      mobile_number: '9900112233',
      email: 'ops@quicklogistics.in',
      pan: 'QKLOG0003C',
      aadhaar_masked: 'XXXXXXXX9012',
      district: 'Pune',
    },
    business: {
      trade_name: 'Quick Logistics Services Pvt Ltd',
      gstin: '27SIMQL0003C1Z1',
      udyam_number: 'UDYAM-MH-20-0034521',
      cin: 'U72900MH2015PTC000003',
      constitution_type: 'Private Limited',
      annual_turnover: '84000000',
      industry_segment: 'Logistics & Supply Chain',
      business_vintage_years: '9',
      employee_count: '215',
      existing_banking: 'ICICI Bank, Axis Bank'
    }
  }
};
const CONSTITUTION_TYPES = ['Proprietorship', 'Partnership', 'LLP', 'Private Limited', 'Public Limited', 'Cooperative', 'Trust'];
const INDUSTRIES = ['Agriculture', 'Manufacturing – Textiles', 'Manufacturing – Auto', 'Retail Trade', 'Logistics & Supply Chain', 'Healthcare', 'Technology', 'Construction'];
const DOC_TYPES = ['PAN', 'AADHAAR', 'GST_CERT', 'UDYAM', 'BANK_STMT', 'FINANCIALS', 'COI'];
const STATES = ['Andhra Pradesh', 'Assam', 'Bihar', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Punjab', 'Rajasthan', 'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'West Bengal'];

const EMPTY_CUSTOMER: CustomerForm = {
  legal_name: '', pan: '', aadhaar_masked: '', mobile_number: '', email: '',
  district: '', persona_name: '', onboarding_status: 'DRAFT',
  address_line1: '', state: '', pincode: ''
};

const EMPTY_BUSINESS: BusinessForm = {
  trade_name: '', gstin: '', udyam_number: '', cin: '',
  constitution_type: '', annual_turnover: '', industry_segment: '',
  business_vintage_years: '', employee_count: '', existing_banking: ''
};

// ── Helpers ───────────────────────────────────────────────────────────────────

const API = apiUrl('');

async function apiFetch(path: string, opts: RequestInit = {}) {
  try {
    const r = await fetch(`${API}${path}`, { headers: { 'Content-Type': 'application/json' }, ...opts });
    return { ok: r.ok, status: r.status, data: await r.json() };
  } catch {
    // Offline / demo mode — return mock success
    return { ok: true, status: 200, data: {} };
  }
}

function panValid(v: string) { return /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(v); }
function gstinValid(v: string) { return /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/.test(v); }
function mobileValid(v: string) { return /^\d{10}$/.test(v); }
function emailValid(v: string) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }
function pincodeValid(v: string) { return /^\d{6}$/.test(v); }
function positiveIntegerValid(v: string) { return /^\d+$/.test(v) && Number(v) >= 0; }

// ── Component ─────────────────────────────────────────────────────────────────

const CustomerOnboardingPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [customer, setCustomer] = useState<CustomerForm>(EMPTY_CUSTOMER);
  const [business, setBusiness] = useState<BusinessForm>(EMPTY_BUSINESS);
  const [documents, setDocuments] = useState<UploadedDoc[]>([]);
  const [validationResults, setValidationResults] = useState<ValidationResult[]>([]);
  const [workflowResult, setWorkflowResult] = useState<Record<string, unknown> | null>(null);
  const [customerId, setCustomerId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [personaLoading, setPersonaLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // ── Persona Load ────────────────────────────────────────────────────────────

  const handleLoadPersona = async (personaName: string) => {
    setPersonaLoading(true);
    setError(null);
    const requestPath = '/customers/load-persona';
    console.info(`[AAROHAN] Persona lookup request URL: ${apiUrl(requestPath)}`);
    const res = await apiFetch(requestPath, {
      method: 'POST', body: JSON.stringify({ persona_name: personaName })
    });
    if (res.ok && res.data?.persona) {
      const p = res.data.persona;
      setCustomer({
        legal_name: p.legal_name ?? '',
        pan: p.pan ?? '',
        aadhaar_masked: p.aadhaar_masked ?? '',
        mobile_number: p.mobile_number ?? '',
        email: p.email ?? '',
        district: p.district ?? '',
        persona_name: personaName,
        onboarding_status: 'DRAFT',
        address_line1: '', state: '', pincode: ''
      });
      if (p.business) {
        setBusiness({
          trade_name: p.business.trade_name ?? '',
          gstin: p.business.gstin ?? '',
          udyam_number: p.business.udyam_number ?? '',
          cin: p.business.cin ?? '',
          constitution_type: p.business.constitution_type ?? '',
          annual_turnover: String(p.business.annual_turnover ?? ''),
          industry_segment: p.business.industry_segment ?? '',
          business_vintage_years: String(p.business.business_vintage_years ?? ''),
          employee_count: String(p.business.employee_count ?? ''),
          existing_banking: p.business.existing_banking ?? ''
        });
      }
      setSuccess(`✓ Persona loaded: ${personaName}`);
    } else {
      const fallback = PERSONA_FALLBACKS[personaName];
      if (fallback) {
        setCustomer((current) => ({
          ...current,
          ...fallback.customer,
          persona_name: personaName,
          onboarding_status: 'DRAFT'
        }));
        setBusiness((current) => ({
          ...current,
          ...fallback.business
        }));
        setSuccess(`✓ Persona loaded from local dataset: ${personaName}`);
      } else {
        setError('Persona not found. Check Simulation Dataset.');
      }
    }
    setPersonaLoading(false);
  };

  // ── Validation ──────────────────────────────────────────────────────────────

  const runValidation = async () => {
    setLoading(true);
    const results: ValidationResult[] = [
      { field: 'pan', valid: panValid(customer.pan), message: panValid(customer.pan) ? 'PAN format valid.' : 'PAN must be 5 letters + 4 digits + 1 letter.' },
      { field: 'mobile_number', valid: mobileValid(customer.mobile_number), message: mobileValid(customer.mobile_number) ? 'Mobile valid.' : 'Mobile must be 10 digits.' },
      { field: 'email', valid: emailValid(customer.email), message: emailValid(customer.email) ? 'Email valid.' : 'Invalid email address.' },
      { field: 'pincode', valid: pincodeValid(customer.pincode), message: pincodeValid(customer.pincode) ? 'Pincode valid.' : 'Pincode must be 6 digits.' },
      { field: 'gstin', valid: gstinValid(business.gstin), message: gstinValid(business.gstin) ? 'GSTIN format valid.' : 'Invalid GSTIN format.' },
      { field: 'trade_name', valid: business.trade_name.trim().length > 0, message: business.trade_name.trim().length > 0 ? 'Business name captured.' : 'Business name is required.' },
      { field: 'constitution_type', valid: business.constitution_type.trim().length > 0, message: business.constitution_type.trim().length > 0 ? 'Entity type captured.' : 'Entity type is required.' },
      { field: 'industry_segment', valid: business.industry_segment.trim().length > 0, message: business.industry_segment.trim().length > 0 ? 'Industry captured.' : 'Industry is required.' },
      { field: 'annual_turnover', valid: positiveIntegerValid(business.annual_turnover) || business.annual_turnover.trim() === '', message: positiveIntegerValid(business.annual_turnover) || business.annual_turnover.trim() === '' ? 'Turnover format accepted.' : 'Annual turnover must be a numeric value.' },
      { field: 'business_vintage_years', valid: positiveIntegerValid(business.business_vintage_years) || business.business_vintage_years.trim() === '', message: positiveIntegerValid(business.business_vintage_years) || business.business_vintage_years.trim() === '' ? 'Vintage format accepted.' : 'Business vintage must be a numeric value.' },
      { field: 'employee_count', valid: positiveIntegerValid(business.employee_count) || business.employee_count.trim() === '', message: positiveIntegerValid(business.employee_count) || business.employee_count.trim() === '' ? 'Employee count accepted.' : 'Employee count must be a numeric value.' },
    ];

    // Remote duplicate check
    const remoteRes = await apiFetch('/customers/validate', {
      method: 'POST',
      body: JSON.stringify({ pan: customer.pan, mobile_number: customer.mobile_number, legal_name: customer.legal_name })
    });
    if (remoteRes.ok && remoteRes.data?.results) {
      const remoteResults: ValidationResult[] = remoteRes.data.results;
      const dupPan = remoteResults.find(r => r.field === 'pan_duplicate');
      const dupMob = remoteResults.find(r => r.field === 'mobile_duplicate');
      if (dupPan) results.push(dupPan);
      if (dupMob) results.push(dupMob);
    }

    setValidationResults(results);
    setLoading(false);
    return results.every(r => r.valid);
  };

  // ── Registration ────────────────────────────────────────────────────────────

  const handleRegister = async () => {
    setLoading(true);
    setError(null);
    const payload = {
      legal_name: customer.legal_name,
      mobile_number: customer.mobile_number,
      email: customer.email,
      pan: customer.pan,
      aadhaar_masked: customer.aadhaar_masked || null,
      district: customer.district || null,
      persona_name: customer.persona_name || null,
      onboarding_status: 'DRAFT',
      businesses: [{
        trade_name: business.trade_name,
        gstin: business.gstin,
        udyam_number: business.udyam_number || null,
        cin: business.cin || null,
        constitution_type: business.constitution_type,
        annual_turnover: parseFloat(business.annual_turnover) || 0,
        industry_segment: business.industry_segment,
        business_vintage_years: parseInt(business.business_vintage_years) || 0,
        employee_count: parseInt(business.employee_count) || 0,
        existing_banking: business.existing_banking || null,
        lifecycle_state: 'REGISTERED',
        directors: []
      }],
      addresses: [{
        address_line1: customer.address_line1,
        city: customer.district || 'Unknown',
        state: customer.state,
        pincode: customer.pincode,
        address_type: 'OFFICE'
      }]
    };
    const res = await apiFetch('/customers', { method: 'POST', body: JSON.stringify(payload) });
    if (res.ok) {
      const registeredId = res.data?.id || Math.floor(Math.random() * 10000);
      setCustomerId(registeredId);
      setSuccess(`✓ Customer registered successfully! ID: ${registeredId}`);
      setTimeout(() => setActiveStep(3), 1000);
    } else if (res.status === 409) {
      setError('Duplicate customer detected. PAN or Mobile already registered.');
    } else {
      // Demo/offline mode fallback
      setCustomerId(9001);
      setSuccess('✓ Customer registered (demo mode).');
    }
    setLoading(false);
  };

  // ── Document Upload ─────────────────────────────────────────────────────────

  const handleDocUpload = async (docType: string, source: 'UPLOAD' | 'SIMULATION_DATASET') => {
    const doc: UploadedDoc = {
      doc_type: docType, doc_name: `${docType}_${customer.pan}.pdf`,
      source, status: 'PENDING'
    };
    if (customerId) {
      await apiFetch(`/customers/${customerId}/documents`, {
        method: 'POST', body: JSON.stringify({ doc_type: docType, doc_name: doc.doc_name, source })
      });
    }
    setDocuments(prev => [...prev.filter(d => d.doc_type !== docType), doc]);
  };

  // ── Workflow Trigger ────────────────────────────────────────────────────────

  const handleStartWorkflow = async () => {
    setLoading(true);
    const cid = customerId ?? 9001;
    const res = await apiFetch(`/customers/${cid}/start-workflow`, { method: 'POST' });
    if (res.ok && res.data?.workflow_id) {
      setWorkflowResult(res.data);
      setSuccess(`✓ MSME Lending Journey started! Workflow ID: ${res.data.workflow_id}`);
    } else {
      // Demo mode
      setWorkflowResult({
        workflow_id: 'wf_demo00000001',
        template_name: 'MSME Lending Journey',
        status: 'STARTED',
        customer_id: cid,
        events_published: ['Customer Registered', 'Business Registered', 'Workflow Started']
      });
      setSuccess('✓ MSME Lending Journey started (demo mode)!');
    }
    setLoading(false);
  };

  // ── Step Navigation ─────────────────────────────────────────────────────────

  const handleNext = async () => {
    setError(null);
    setSuccess(null);
    if (activeStep === 2) {
      const valid = await runValidation();
      setActiveStep(3);
      if (!valid) { setError('Please fix validation errors before continuing.'); return; }
      return;
    }
    if (activeStep === 3) {
      if (validationResults.length > 0 && !validationResults.every(r => r.valid)) {
        setError('Please resolve all validation errors before registering the customer.');
        return;
      }
      await handleRegister();
    }
    if (activeStep === 4) { await handleStartWorkflow(); }
    setActiveStep(s => s + 1);
  };

  const handleBack = () => { setError(null); setSuccess(null); setActiveStep(s => s - 1); };

  // ── Render Helpers ──────────────────────────────────────────────────────────

  const fieldStyle = { mb: 2 };

  const ValidationChip = ({ result }: { result: ValidationResult }) => (
    <Chip
      key={result.field}
      size="small"
      icon={result.valid ? <CheckCircle fontSize="small" /> : <Warning fontSize="small" />}
      label={`${result.field}: ${result.message}`}
      color={result.valid ? 'success' : 'error'}
      sx={{ m: 0.5, fontSize: '0.7rem' }}
    />
  );

  // ── Step Content Panels ─────────────────────────────────────────────────────

  const stepPanels = [

    /* ── Step 0: Persona Selection ─────────────────────────────────────────── */
    <Box>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Select an existing ESE Persona to auto-populate the onboarding form, or proceed as a new customer.
      </Typography>
      <Grid container spacing={1.5}>
        {PERSONAS.map(p => (
          <Grid item xs={12} sm={4} key={p}>
            <Card
              onClick={() => handleLoadPersona(p)}
              sx={{ cursor: 'pointer', border: customer.persona_name === p ? '2px solid #1976d2' : '1px solid #e0e0e0', transition: 'all 0.2s', '&:hover': { boxShadow: 4 } }}
            >
              <CardContent sx={{ p: 2 }}>
                <Avatar sx={{ bgcolor: '#1976d2', mb: 1, width: 32, height: 32, fontSize: '0.85rem' }}>
                  {p[0]}
                </Avatar>
                <Typography variant="subtitle2" fontWeight={600}>{p}</Typography>
                <Typography variant="caption" color="text.secondary">ESE Persona</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      {personaLoading && <LinearProgress sx={{ mt: 2 }} />}
      {customer.persona_name && (
        <Alert severity="success" sx={{ mt: 2 }}>
          Persona <strong>{customer.persona_name}</strong> loaded. Form pre-populated.
        </Alert>
      )}
      <Button startIcon={<Person />} variant="outlined" sx={{ mt: 2 }} onClick={() => { setCustomer(EMPTY_CUSTOMER); setBusiness(EMPTY_BUSINESS); }}>
        New Customer (Empty Form)
      </Button>
    </Box>,

    /* ── Step 1: Customer Registration ─────────────────────────────────────── */
    <Box>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}><TextField fullWidth label="Applicant Name *" value={customer.legal_name} onChange={e => setCustomer(c => ({ ...c, legal_name: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="PAN *" value={customer.pan} onChange={e => setCustomer(c => ({ ...c, pan: e.target.value.toUpperCase() }))} helperText="Format: AAAAA9999A" sx={fieldStyle} error={customer.pan.length > 0 && !panValid(customer.pan)} /></Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="Aadhaar (Demo)" value={customer.aadhaar_masked} onChange={e => setCustomer(c => ({ ...c, aadhaar_masked: e.target.value }))} helperText="Masked: XXXXXXXX1234" sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="Mobile *" value={customer.mobile_number} onChange={e => setCustomer(c => ({ ...c, mobile_number: e.target.value }))} sx={fieldStyle} error={customer.mobile_number.length > 0 && !mobileValid(customer.mobile_number)} /></Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="Email *" type="email" value={customer.email} onChange={e => setCustomer(c => ({ ...c, email: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="District" value={customer.district} onChange={e => setCustomer(c => ({ ...c, district: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12}><Divider sx={{ my: 1 }}><Typography variant="caption" color="text.secondary">Address</Typography></Divider></Grid>
        <Grid item xs={12}><TextField fullWidth label="Address Line 1 *" value={customer.address_line1} onChange={e => setCustomer(c => ({ ...c, address_line1: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={6}>
          <TextField select fullWidth label="State *" value={customer.state} onChange={e => setCustomer(c => ({ ...c, state: e.target.value }))} sx={fieldStyle}>
            {STATES.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="Pincode *" value={customer.pincode} onChange={e => setCustomer(c => ({ ...c, pincode: e.target.value }))} sx={fieldStyle} error={customer.pincode.length > 0 && !pincodeValid(customer.pincode)} /></Grid>
      </Grid>
    </Box>,

    /* ── Step 2: Business Registration ─────────────────────────────────────── */
    <Box>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}><TextField fullWidth label="Business Name *" value={business.trade_name} onChange={e => setBusiness(b => ({ ...b, trade_name: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={6}>
          <TextField select fullWidth label="Entity Type *" value={business.constitution_type} onChange={e => setBusiness(b => ({ ...b, constitution_type: e.target.value }))} sx={fieldStyle}>
            {CONSTITUTION_TYPES.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="GSTIN *" value={business.gstin} onChange={e => setBusiness(b => ({ ...b, gstin: e.target.value.toUpperCase() }))} helperText="27AABCU9603R1ZX" sx={fieldStyle} error={business.gstin.length > 0 && !gstinValid(business.gstin)} /></Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="UDYAM Number" value={business.udyam_number} onChange={e => setBusiness(b => ({ ...b, udyam_number: e.target.value }))} helperText="UDYAM-XX-00-0000000" sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={6}><TextField fullWidth label="CIN (if applicable)" value={business.cin} onChange={e => setBusiness(b => ({ ...b, cin: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={6}>
          <TextField select fullWidth label="Industry *" value={business.industry_segment} onChange={e => setBusiness(b => ({ ...b, industry_segment: e.target.value }))} sx={fieldStyle}>
            {INDUSTRIES.map(i => <MenuItem key={i} value={i}>{i}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item xs={12} sm={4}><TextField fullWidth label="Annual Turnover (₹)" type="number" value={business.annual_turnover} onChange={e => setBusiness(b => ({ ...b, annual_turnover: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={4}><TextField fullWidth label="Business Vintage (Years)" type="number" value={business.business_vintage_years} onChange={e => setBusiness(b => ({ ...b, business_vintage_years: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12} sm={4}><TextField fullWidth label="Employees" type="number" value={business.employee_count} onChange={e => setBusiness(b => ({ ...b, employee_count: e.target.value }))} sx={fieldStyle} /></Grid>
        <Grid item xs={12}><TextField fullWidth label="Existing Banking Relationship" value={business.existing_banking} onChange={e => setBusiness(b => ({ ...b, existing_banking: e.target.value }))} helperText="e.g. SBI, HDFC Bank" sx={fieldStyle} /></Grid>
      </Grid>
    </Box>,

    /* ── Step 3: Validation ─────────────────────────────────────────────────── */
    <Box>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Click Validate to check field formats and detect duplicate registrations.
      </Typography>
      <Button variant="outlined" onClick={runValidation} disabled={loading} startIcon={<Search />} sx={{ mb: 2 }}>
        {loading ? 'Validating…' : 'Run Validation'}
      </Button>
      {loading && <LinearProgress sx={{ mb: 2 }} />}
      {validationResults.length > 0 && (
        <Box>
          <Box sx={{ mb: 1 }}>
            {validationResults.map(r => <ValidationChip key={r.field} result={r} />)}
          </Box>
          {validationResults.every(r => r.valid)
            ? <Alert severity="success" icon={<CheckCircle />}>All validations passed — ready to register.</Alert>
            : <Alert severity="error" icon={<Warning />}>Fix errors above before proceeding.</Alert>
          }
        </Box>
      )}
    </Box>,

    /* ── Step 4: Document Upload ─────────────────────────────────────────────── */
    <Box>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Upload documents or load directly from the Simulation Dataset.
      </Typography>
      <Table size="small" sx={{ mb: 2 }}>
        <TableHead>
          <TableRow>
            <TableCell><strong>Document Type</strong></TableCell>
            <TableCell><strong>Status</strong></TableCell>
            <TableCell><strong>Source</strong></TableCell>
            <TableCell><strong>Actions</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {DOC_TYPES.map(dt => {
            const uploaded = documents.find(d => d.doc_type === dt);
            return (
              <TableRow key={dt}>
                <TableCell>{dt.replace('_', ' ')}</TableCell>
                <TableCell>
                  {uploaded
                    ? <Chip size="small" label="Uploaded" color="success" icon={<CheckCircle fontSize="small" />} />
                    : <Chip size="small" label="Pending" color="default" />}
                </TableCell>
                <TableCell>{uploaded?.source ?? '–'}</TableCell>
                <TableCell>
                  <Tooltip title="Simulate Upload">
                    <IconButton size="small" onClick={() => handleDocUpload(dt, 'UPLOAD')}><UploadFile fontSize="small" /></IconButton>
                  </Tooltip>
                  <Tooltip title="Load from Simulation Dataset">
                    <IconButton size="small" onClick={() => handleDocUpload(dt, 'SIMULATION_DATASET')} color="primary"><Refresh fontSize="small" /></IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
      <Alert severity="info" icon={<Info />}>
        {documents.length} of {DOC_TYPES.length} documents uploaded.
      </Alert>
    </Box>,

    /* ── Step 5: Customer Dashboard ─────────────────────────────────────────── */
    <Box>
      {workflowResult ? (
        <>
          <Alert severity="success" icon={<CheckCircle />} sx={{ mb: 2 }}>
            <strong>MSME Lending Journey Started!</strong><br />
            Workflow ID: <code>{String(workflowResult.workflow_id ?? '')}</code>
          </Alert>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" fontWeight={700} gutterBottom>Customer Profile</Typography>
                <Typography variant="body2"><strong>Name:</strong> {customer.legal_name}</Typography>
                <Typography variant="body2"><strong>PAN:</strong> {customer.pan}</Typography>
                <Typography variant="body2"><strong>Mobile:</strong> {customer.mobile_number}</Typography>
                <Typography variant="body2"><strong>Email:</strong> {customer.email}</Typography>
                <Typography variant="body2"><strong>District:</strong> {customer.district}</Typography>
                <Typography variant="body2" sx={{ mt: 1 }}><strong>Status:</strong> <Chip size="small" label="SUBMITTED" color="primary" /></Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" fontWeight={700} gutterBottom>Business Profile</Typography>
                <Typography variant="body2"><strong>Business:</strong> {business.trade_name}</Typography>
                <Typography variant="body2"><strong>GSTIN:</strong> {business.gstin}</Typography>
                <Typography variant="body2"><strong>UDYAM:</strong> {business.udyam_number || '–'}</Typography>
                <Typography variant="body2"><strong>Industry:</strong> {business.industry_segment}</Typography>
                <Typography variant="body2"><strong>Turnover:</strong> ₹{Number(business.annual_turnover || 0).toLocaleString('en-IN')}</Typography>
                <Typography variant="body2"><strong>Employees:</strong> {business.employee_count}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" fontWeight={700} gutterBottom>Events Published</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {(workflowResult.events_published as string[])?.map(evt => (
                    <Chip key={evt} label={evt} color="success" size="small" icon={<CheckCircle fontSize="small" />} />
                  ))}
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" fontWeight={700} gutterBottom>Documents ({documents.length})</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {documents.map(d => (
                    <Chip key={d.doc_type} label={`${d.doc_type} (${d.source})`} size="small" color="default" />
                  ))}
                  {documents.length === 0 && <Typography variant="caption" color="text.secondary">No documents uploaded</Typography>}
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </>
      ) : (
        <Alert severity="info">Click Next to start the MSME Lending Journey workflow.</Alert>
      )}
    </Box>
  ];

  const STEPS = [
    { label: 'Persona Selection', icon: <Person /> },
    { label: 'Customer Registration', icon: <Person /> },
    { label: 'Business Registration', icon: <Business /> },
    { label: 'Validation', icon: <CheckCircle /> },
    { label: 'Document Upload', icon: <UploadFile /> },
    { label: 'Customer Dashboard', icon: <PlayArrow /> },
  ];

  return (
    <Box sx={{ p: 3, maxWidth: 900, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={700} gutterBottom>
          Enterprise Customer Onboarding
        </Typography>
        <Typography variant="body2" color="text.secondary">
          MSME Customer Registration · Business KYC · Document Upload · Workflow Launch
        </Typography>
      </Box>

      {/* Alerts */}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>{success}</Alert>}
      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {/* Stepper */}
      <Stepper activeStep={activeStep} orientation="vertical">
        {STEPS.map((step, idx) => (
          <Step key={step.label}>
            <StepLabel
              StepIconProps={{
                sx: {
                  color: idx < activeStep ? 'success.main' : idx === activeStep ? 'primary.main' : 'text.disabled',
                }
              }}
            >
              <Typography fontWeight={idx === activeStep ? 700 : 400}>{step.label}</Typography>
            </StepLabel>
            <StepContent>
              <Box sx={{ mb: 2 }}>{stepPanels[idx]}</Box>
              <Box sx={{ display: 'flex', gap: 1 }}>
                {idx > 0 && (
                  <Button onClick={handleBack} startIcon={<ArrowBack />} variant="outlined" size="small">
                    Back
                  </Button>
                )}
                {idx < STEPS.length - 1 && (
                  <Button onClick={handleNext} endIcon={<ArrowForward />} variant="contained" size="small" disabled={loading}>
                    {idx === 3 ? 'Register Customer' : idx === 4 ? 'Start Journey' : 'Next'}
                  </Button>
                )}
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>

      {/* Done state */}
      {activeStep === STEPS.length && (
        <Alert severity="success" icon={<CheckCircle />} sx={{ mt: 2 }}>
          <strong>Onboarding Complete!</strong> Customer registered and MSME Lending Journey launched.
        </Alert>
      )}
    </Box>
  );
};

export default CustomerOnboardingPage;
