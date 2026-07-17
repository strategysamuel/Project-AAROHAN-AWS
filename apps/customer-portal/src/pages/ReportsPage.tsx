import React from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  LinearProgress,
  Paper,
  Stack,
  Typography
} from '@mui/material';
import { Download, Description, FolderZip, Receipt, Gavel, Assessment, BarChart } from '@mui/icons-material';
import { apiUrl } from '../lib/api';
import { downloadTextFile } from '../lib/download';

const API = apiUrl('');

type ReportSpec = {
  label: string;
  reportType: string;
  fileName: string;
  description: string;
  icon: React.ReactNode;
};

const REPORTS: ReportSpec[] = [
  { label: 'Financial Health Card', reportType: 'FHC', fileName: 'AAROHAN_FHC_RC1.md', description: 'Explainable score and risk summary.', icon: <Assessment /> },
  { label: 'Credit Decision', reportType: 'CREDIT', fileName: 'AAROHAN_CREDIT_DECISION_RC1.md', description: 'Underwriting recommendation and rationale.', icon: <Gavel /> },
  { label: 'CAM', reportType: 'CAM', fileName: 'AAROHAN_CAM_RC1.md', description: 'Credit appraisal memo for reviewers.', icon: <Description /> },
  { label: 'Executive Summary', reportType: 'RECOMMENDATION', fileName: 'AAROHAN_EXECUTIVE_SUMMARY_RC1.md', description: 'Board-ready executive summary.', icon: <BarChart /> },
  { label: 'Portfolio Report', reportType: 'PORTFOLIO', fileName: 'AAROHAN_PORTFOLIO_SUMMARY_RC1.md', description: 'Portfolio mix and concentration snapshot.', icon: <FolderZip /> },
  { label: 'Fraud Report', reportType: 'RISK', fileName: 'AAROHAN_FRAUD_REPORT_RC1.md', description: 'Fraud and early warning summary.', icon: <Receipt /> }
];

const ReportsPage: React.FC = () => {
  const [loadingReport, setLoadingReport] = React.useState<string | null>(null);
  const [message, setMessage] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const downloadReport = async (report: ReportSpec) => {
    setLoadingReport(report.reportType);
    setMessage(null);
    setError(null);
    try {
      const response = await fetch(apiUrl('/ese/control/report'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          report_type: report.reportType,
          format_type: 'MARKDOWN',
          data: {
            customer_id: 99,
            persona: 'RC1 Demo',
            scenario: 'Release Candidate',
            dataset: 'msme',
            active_page: 'Reports',
            release: 'AAR-BUILD-020 RC1'
          }
        })
      });

      if (!response.ok) {
        throw new Error(`Report generation failed with status ${response.status}`);
      }

      const payload = await response.json();
      const content = typeof payload.content === 'string'
        ? payload.content
        : `# Project AAROHAN - ${report.label}\n\nGenerated from the active RC1 report pack.`;
      downloadTextFile(report.fileName, content, 'text/markdown');
      setMessage(`${report.label} downloaded as ${report.fileName}.`);
    } catch (exc: any) {
      const fallback = `# Project AAROHAN - ${report.label}\n\nThe live report endpoint was unavailable, so this RC1 fallback was generated locally.`;
      downloadTextFile(report.fileName, fallback, 'text/markdown');
      setMessage(`${report.label} downloaded from local fallback.`);
      setError(exc?.message ? `${exc.message}. Fallback file generated instead.` : 'Fallback file generated instead.');
    } finally {
      setLoadingReport(null);
    }
  };

  return (
    <Box sx={{ p: 1 }}>
      <Typography variant="h5" fontWeight="bold" sx={{ mb: 1 }}>Reports</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Generate the RC1 report pack directly from the active demo state.
      </Typography>

      {loadingReport && <LinearProgress sx={{ mb: 2 }} />}
      {message && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage(null)}>{message}</Alert>}
      {error && <Alert severity="warning" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Grid container spacing={3}>
        {REPORTS.map((report) => (
          <Grid item xs={12} sm={6} md={4} key={report.reportType}>
            <Card variant="outlined" sx={{ height: '100%' }}>
              <CardContent sx={{ p: 2.5, height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start" spacing={2} sx={{ mb: 1 }}>
                  <Box>
                    <Typography variant="subtitle2" fontWeight="bold">{report.label}</Typography>
                    <Typography variant="caption" color="text.secondary">{report.description}</Typography>
                  </Box>
                  <Box sx={{ color: 'primary.main' }}>{report.icon}</Box>
                </Stack>
                <Box sx={{ flexGrow: 1 }} />
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<Download />}
                  onClick={() => downloadReport(report)}
                  disabled={loadingReport === report.reportType}
                  sx={{ mt: 2 }}
                >
                  Download
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ p: 3, mt: 3, border: '1px solid rgba(255,255,255,0.06)' }}>
        <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 1 }}>Report validation</Typography>
        <Typography variant="body2" color="text.secondary">
          Each button triggers the live report generator, downloads a file with the intended filename, and falls back to a local RC1 markdown file if the backend is unavailable.
        </Typography>
      </Paper>
    </Box>
  );
};

export default ReportsPage;