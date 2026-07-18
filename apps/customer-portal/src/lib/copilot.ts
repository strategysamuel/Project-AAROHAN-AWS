import { apiUrl } from './api';

const API = apiUrl('');

export type CopilotRole = 'CUSTOMER' | 'RELATIONSHIP_MANAGER' | 'CREDIT_MANAGER' | 'EXECUTIVE' | 'ADMINISTRATOR' | 'DEMO_USER' | string;

export type CopilotSuggestion = {
  label: string;
  prompt: string;
};

export type CopilotRoleKey =
  | 'ADMINISTRATOR'
  | 'EXECUTIVE'
  | 'RELATIONSHIP_MANAGER'
  | 'CREDIT_MANAGER'
  | 'CREDIT_UNDERWRITER'
  | 'RISK_OFFICER'
  | 'OPERATIONS_OFFICER'
  | 'COMPLIANCE_OFFICER'
  | 'CUSTOMER'
  | 'AUDITOR'
  | 'TRAINER'
  | 'DEMO_USER';

export type CopilotHomeSection = {
  title: string;
  items: string[];
};

export type CopilotRoleProfile = {
  key: CopilotRoleKey;
  title: string;
  subtitle: string;
  badge: string;
  segment: string;
  suggestedPrompts: string[];
  quickCommands: string[];
  recommendedReports: string[];
  frequentlyUsedTasks: string[];
  pinnedActions: string[];
  homeSections: CopilotHomeSection[];
  permissions: string[];
};

export type CopilotContext = {
  role: CopilotRole;
  activePage: string;
  activePersona: string;
  activeScenario: string;
  activeDataset: string;
  userName?: string;
};

export type CopilotAction =
  | { type: 'navigate'; page: string }
  | { type: 'download-report'; reportType: string }
  | { type: 'download-pack'; reportTypes: string[] }
  | { type: 'toast'; message: string; severity?: 'success' | 'info' | 'warning' | 'error' };

export type CopilotTurn = {
  intent: string;
  reply: string;
  actions: CopilotAction[];
  evidence?: string[];
};

export type ReportSpec = {
  label: string;
  reportType: string;
  fileName: string;
  description: string;
};

export const REPORT_PACK: ReportSpec[] = [
  { label: 'Financial Health Card', reportType: 'FHC', fileName: 'AAROHAN_FHC_RC1.md', description: 'Explainable score and risk summary.' },
  { label: 'Credit Decision', reportType: 'CREDIT', fileName: 'AAROHAN_CREDIT_DECISION_RC1.md', description: 'Underwriting recommendation and rationale.' },
  { label: 'CAM', reportType: 'CAM', fileName: 'AAROHAN_CAM_RC1.md', description: 'Credit appraisal memo for reviewers.' },
  { label: 'Executive Summary', reportType: 'RECOMMENDATION', fileName: 'AAROHAN_EXECUTIVE_SUMMARY_RC1.md', description: 'Board-ready executive summary.' },
  { label: 'Portfolio Report', reportType: 'PORTFOLIO', fileName: 'AAROHAN_PORTFOLIO_SUMMARY_RC1.md', description: 'Portfolio mix and concentration snapshot.' },
  { label: 'Fraud Report', reportType: 'RISK', fileName: 'AAROHAN_FRAUD_REPORT_RC1.md', description: 'Fraud and early warning summary.' }
];

export const ROLE_REPORT_ACCESS: Record<CopilotRoleKey, string[]> = {
  ADMINISTRATOR: ['RECOMMENDATION', 'PORTFOLIO', 'RISK'],
  EXECUTIVE: ['RECOMMENDATION', 'PORTFOLIO', 'RISK'],
  RELATIONSHIP_MANAGER: ['FHC', 'CREDIT', 'CAM'],
  CREDIT_MANAGER: ['FHC', 'CREDIT', 'CAM', 'RISK'],
  CREDIT_UNDERWRITER: ['FHC', 'CREDIT', 'CAM', 'RISK'],
  RISK_OFFICER: ['RISK', 'PORTFOLIO'],
  OPERATIONS_OFFICER: ['FHC'],
  COMPLIANCE_OFFICER: ['RISK'],
  CUSTOMER: ['FHC'],
  AUDITOR: ['RECOMMENDATION', 'RISK'],
  TRAINER: ['RECOMMENDATION', 'PORTFOLIO', 'CAM'],
  DEMO_USER: ['FHC', 'CAM', 'RECOMMENDATION']
};

type CopilotConfig = {
  enabled: boolean;
  voiceEnabled: boolean;
  provider: string;
  apiKey: string;
  model: string;
  endpoint: string;
};

export const ROLE_PROFILES: Record<CopilotRoleKey, CopilotRoleProfile> = {
  ADMINISTRATOR: {
    key: 'ADMINISTRATOR',
    title: 'Administrator',
    subtitle: 'Platform control and demo governance',
    badge: 'Admin',
    segment: 'Platform Operations',
    suggestedPrompts: ['Reset Demo', 'Load Persona', 'Switch Scenario', 'Manage Users', 'System Health', 'Dataset Status', 'Simulation Status', 'Cloud Status', 'Logs'],
    quickCommands: ['Reset demo', 'Load persona', 'Switch scenario', 'Show system health'],
    recommendedReports: ['Executive Summary', 'Portfolio Report', 'Fraud Report'],
    frequentlyUsedTasks: ['Reset demo', 'Load persona', 'Switch scenario', 'Inspect logs'],
    pinnedActions: ['Reset Demo', 'Load Persona', 'System Health'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Reset demo', 'Load persona', 'Switch scenario', 'Manage users'] },
      { title: 'Quick Commands', items: ['System health', 'Dataset status', 'Simulation status', 'Cloud status'] },
      { title: 'Recommended Reports', items: ['Executive Summary', 'Portfolio Report', 'Fraud Report'] },
      { title: 'Frequently Used Tasks', items: ['Reset demo', 'Load persona', 'Logs', 'Dataset status'] },
      { title: 'Pinned Actions', items: ['Reset Demo', 'Load Persona', 'Cloud Status'] }
    ],
    permissions: ['admin', 'dashboard', 'reports', 'settings', 'simulation', 'users', 'system']
  },
  EXECUTIVE: {
    key: 'EXECUTIVE',
    title: 'Executive',
    subtitle: 'MSME lending and portfolio leadership',
    badge: 'Executive',
    segment: 'MSME Lending',
    suggestedPrompts: ['Today\'s MSME Portfolio', 'Portfolio Exposure', 'Approval Rate', 'Sector-wise Lending', 'Top Performing Branches', 'Largest Sanctions', 'Rejected Applications', 'Risk Heatmap', 'Executive Summary', 'Generate Board Report'],
    quickCommands: ['Open Executive Dashboard', 'Generate Board Report', 'Show risk heatmap', 'Show approval rate'],
    recommendedReports: ['Executive Summary', 'Portfolio Report', 'Risk Summary', 'Board Dashboard'],
    frequentlyUsedTasks: ['Portfolio exposure', 'Top branches', 'Rejected applications', 'Board report'],
    pinnedActions: ['Open Executive Dashboard', 'Generate Board Report', 'Risk Heatmap'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Today\'s MSME portfolio', 'Portfolio exposure', 'Approval rate', 'Risk heatmap'] },
      { title: 'Quick Commands', items: ['Open dashboard', 'Generate board report', 'Show sector-wise lending', 'Show top branches'] },
      { title: 'Recommended Reports', items: ['Executive Summary', 'Portfolio Report', 'Risk Summary', 'Board Dashboard'] },
      { title: 'Frequently Used Tasks', items: ['Rejected applications', 'Largest sanctions', 'Approval rate', 'Board report'] },
      { title: 'Pinned Actions', items: ['Open Executive Dashboard', 'Generate Board Report', 'Portfolio Exposure'] }
    ],
    permissions: ['dashboard', 'reports', 'portfolio', 'risk', 'analytics']
  },
  RELATIONSHIP_MANAGER: {
    key: 'RELATIONSHIP_MANAGER',
    title: 'Relationship Manager',
    subtitle: 'Commercial banking and customer operations',
    badge: 'RM',
    segment: 'Commercial Banking',
    suggestedPrompts: ['Show pending customers', 'Open onboarding', 'Generate CAM', 'Compare borrowers', 'Show GST compliance', 'Show Financial Health Card', 'Run underwriting', 'Open Customer Profile', "Show today's meetings"],
    quickCommands: ['Open onboarding', 'Generate CAM', 'Open customer profile', 'Show GST compliance'],
    recommendedReports: ['CAM', 'Customer Profile', 'GST Analysis', 'Credit Decision'],
    frequentlyUsedTasks: ['Pending customers', 'Open onboarding', 'Generate CAM', 'Compare borrowers'],
    pinnedActions: ['Open onboarding', 'Generate CAM', 'Show GST compliance'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Show pending customers', 'Open onboarding', 'Generate CAM', 'Compare borrowers'] },
      { title: 'Quick Commands', items: ['Show GST compliance', 'Show Financial Health Card', 'Run underwriting', 'Open customer profile'] },
      { title: 'Recommended Reports', items: ['CAM', 'Customer Profile', 'GST Analysis', 'Credit Decision'] },
      { title: 'Frequently Used Tasks', items: ['Open onboarding', 'Generate CAM', 'Compare borrowers', "Show today's meetings"] },
      { title: 'Pinned Actions', items: ['Open onboarding', 'Generate CAM', 'Open customer profile'] }
    ],
    permissions: ['dashboard', 'customer_management', 'onboarding', 'credit', 'reports', 'gst', 'account_aggregator', 'epfo', 'mca']
  },
  CREDIT_MANAGER: {
    key: 'CREDIT_MANAGER',
    title: 'Credit Manager',
    subtitle: 'Policy, underwriting, and decision governance',
    badge: 'Credit',
    segment: 'Credit Operations',
    suggestedPrompts: ['Pending Approvals', 'Manual Reviews', 'Credit Decision', 'Generate CAM', 'Compare Credit Scores', 'Policy Exceptions', 'Risk Analysis'],
    quickCommands: ['Show pending approvals', 'Generate CAM', 'Show policy exceptions', 'Compare credit scores'],
    recommendedReports: ['Credit Decision', 'CAM', 'Policy Exceptions', 'Risk Summary'],
    frequentlyUsedTasks: ['Manual reviews', 'Generate CAM', 'Credit decision', 'Policy exceptions'],
    pinnedActions: ['Pending approvals', 'Generate CAM', 'Risk analysis'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Pending approvals', 'Manual reviews', 'Credit decision', 'Generate CAM'] },
      { title: 'Quick Commands', items: ['Compare credit scores', 'Policy exceptions', 'Risk analysis', 'Open credit queue'] },
      { title: 'Recommended Reports', items: ['Credit Decision', 'CAM', 'Policy Exceptions', 'Risk Summary'] },
      { title: 'Frequently Used Tasks', items: ['Manual reviews', 'Generate CAM', 'Credit decision', 'Policy exceptions'] },
      { title: 'Pinned Actions', items: ['Pending approvals', 'Generate CAM', 'Open credit queue'] }
    ],
    permissions: ['credit_engine', 'cam', 'reports', 'risk', 'dashboard']
  },
  CREDIT_UNDERWRITER: {
    key: 'CREDIT_UNDERWRITER',
    title: 'Credit Underwriter',
    subtitle: 'Assessment, policy, and recommendation support',
    badge: 'Underwriter',
    segment: 'Underwriting',
    suggestedPrompts: ['Generate CAM', 'Compare borrowers', 'Credit score details', 'Risk grade', 'Policy exceptions', 'Run underwriting'],
    quickCommands: ['Generate CAM', 'Compare borrowers', 'Show risk grade', 'Run underwriting'],
    recommendedReports: ['CAM', 'Credit Decision', 'Risk Summary'],
    frequentlyUsedTasks: ['Generate CAM', 'Compare borrowers', 'Credit score details', 'Policy exceptions'],
    pinnedActions: ['Generate CAM', 'Run underwriting', 'Risk grade'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Generate CAM', 'Compare borrowers', 'Credit score details', 'Run underwriting'] },
      { title: 'Quick Commands', items: ['Policy exceptions', 'Risk grade', 'Financial health card', 'Open credit decision'] },
      { title: 'Recommended Reports', items: ['CAM', 'Credit Decision', 'Risk Summary'] },
      { title: 'Frequently Used Tasks', items: ['Generate CAM', 'Compare borrowers', 'Policy exceptions', 'Run underwriting'] },
      { title: 'Pinned Actions', items: ['Generate CAM', 'Run underwriting', 'Open credit decision'] }
    ],
    permissions: ['credit_engine', 'cam', 'reports', 'dashboard', 'risk']
  },
  RISK_OFFICER: {
    key: 'RISK_OFFICER',
    title: 'Risk Officer',
    subtitle: 'Portfolio risk, alerts, and early warning management',
    badge: 'Risk',
    segment: 'Risk Management',
    suggestedPrompts: ['High Risk Borrowers', 'Early Warning Signals', 'Fraud Cases', 'Portfolio Risk', 'Stress Accounts', 'NPA Prediction', 'Exposure Analysis'],
    quickCommands: ['Show high risk borrowers', 'Show early warning signals', 'Show fraud cases', 'Show exposure analysis'],
    recommendedReports: ['Risk Summary', 'Portfolio Report', 'Fraud Report'],
    frequentlyUsedTasks: ['High risk borrowers', 'Fraud cases', 'Stress accounts', 'Exposure analysis'],
    pinnedActions: ['High Risk Borrowers', 'Early Warning Signals', 'Portfolio Risk'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['High risk borrowers', 'Early warning signals', 'Fraud cases', 'Portfolio risk'] },
      { title: 'Quick Commands', items: ['Stress accounts', 'NPA prediction', 'Exposure analysis', 'Open risk dashboard'] },
      { title: 'Recommended Reports', items: ['Risk Summary', 'Portfolio Report', 'Fraud Report'] },
      { title: 'Frequently Used Tasks', items: ['High risk borrowers', 'Fraud cases', 'Stress accounts', 'Exposure analysis'] },
      { title: 'Pinned Actions', items: ['High Risk Borrowers', 'Portfolio Risk', 'Open risk dashboard'] }
    ],
    permissions: ['risk', 'reports', 'dashboard', 'alerts']
  },
  OPERATIONS_OFFICER: {
    key: 'OPERATIONS_OFFICER',
    title: 'Operations Officer',
    subtitle: 'Case flow, documentation, and service operations',
    badge: 'Ops',
    segment: 'Operations',
    suggestedPrompts: ['Open onboarding', 'Required Documents', 'Pending Cases', 'Workflow Status', 'Document Gaps', 'Disbursal Queue'],
    quickCommands: ['Open onboarding', 'Show required documents', 'Show workflow status', 'Show pending cases'],
    recommendedReports: ['Customer Profile', 'Workflow Summary', 'Documents'],
    frequentlyUsedTasks: ['Pending cases', 'Document gaps', 'Workflow status', 'Disbursal queue'],
    pinnedActions: ['Open onboarding', 'Required Documents', 'Workflow Status'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Open onboarding', 'Required documents', 'Pending cases', 'Workflow status'] },
      { title: 'Quick Commands', items: ['Document gaps', 'Disbursal queue', 'Customer profile', 'Case queue'] },
      { title: 'Recommended Reports', items: ['Customer Profile', 'Workflow Summary', 'Documents'] },
      { title: 'Frequently Used Tasks', items: ['Pending cases', 'Document gaps', 'Workflow status', 'Disbursal queue'] },
      { title: 'Pinned Actions', items: ['Open onboarding', 'Workflow Status', 'Case queue'] }
    ],
    permissions: ['customer_management', 'onboarding', 'documents', 'workflow', 'reports']
  },
  COMPLIANCE_OFFICER: {
    key: 'COMPLIANCE_OFFICER',
    title: 'Compliance Officer',
    subtitle: 'KYC, AML, audit, and regulatory oversight',
    badge: 'Compliance',
    segment: 'Regulatory Control',
    suggestedPrompts: ['KYC Exceptions', 'AML Alerts', 'CKYC Status', 'Audit Reports', 'Regulatory Compliance'],
    quickCommands: ['Show KYC exceptions', 'Show AML alerts', 'Show CKYC status', 'Open audit reports'],
    recommendedReports: ['Audit Reports', 'KYC Exceptions', 'Compliance Summary'],
    frequentlyUsedTasks: ['KYC exceptions', 'AML alerts', 'CKYC status', 'Audit reports'],
    pinnedActions: ['KYC Exceptions', 'AML Alerts', 'Audit Reports'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['KYC exceptions', 'AML alerts', 'CKYC status', 'Audit reports'] },
      { title: 'Quick Commands', items: ['Regulatory compliance', 'Exception review', 'Audit trail', 'Open compliance dashboard'] },
      { title: 'Recommended Reports', items: ['Audit Reports', 'KYC Exceptions', 'Compliance Summary'] },
      { title: 'Frequently Used Tasks', items: ['KYC exceptions', 'AML alerts', 'CKYC status', 'Audit reports'] },
      { title: 'Pinned Actions', items: ['KYC Exceptions', 'AML Alerts', 'Open compliance dashboard'] }
    ],
    permissions: ['kyc', 'aml', 'audit', 'reports', 'dashboard']
  },
  CUSTOMER: {
    key: 'CUSTOMER',
    title: 'Customer',
    subtitle: 'Self-service loan and document assistance',
    badge: 'Customer',
    segment: 'Customer Banking',
    suggestedPrompts: ['Loan Status', 'Application Status', 'Required Documents', 'Eligibility', 'Financial Health Card', 'Download CAM', 'GST Status', 'Support'],
    quickCommands: ['Loan status', 'Required documents', 'Financial health card', 'Support'],
    recommendedReports: ['Financial Health Card', 'Loan Status', 'Documents'],
    frequentlyUsedTasks: ['Loan status', 'Application status', 'Required documents', 'Eligibility'],
    pinnedActions: ['Loan Status', 'Required Documents', 'Financial Health Card'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Loan status', 'Application status', 'Required documents', 'Eligibility'] },
      { title: 'Quick Commands', items: ['Financial health card', 'Download CAM', 'GST status', 'Support'] },
      { title: 'Recommended Reports', items: ['Financial Health Card', 'Loan Status', 'Documents'] },
      { title: 'Frequently Used Tasks', items: ['Loan status', 'Application status', 'Required documents', 'Support'] },
      { title: 'Pinned Actions', items: ['Loan Status', 'Financial Health Card', 'Support'] }
    ],
    permissions: ['dashboard', 'customer_self_service', 'reports', 'documents']
  },
  AUDITOR: {
    key: 'AUDITOR',
    title: 'Auditor',
    subtitle: 'Independent review and evidence tracing',
    badge: 'Audit',
    segment: 'Audit & Assurance',
    suggestedPrompts: ['Audit Trail', 'Decision Evidence', 'Exceptions', 'Report History', 'Document Trace', 'Policy Overrides'],
    quickCommands: ['Open audit trail', 'Show decision evidence', 'Show exceptions', 'Show report history'],
    recommendedReports: ['Audit Reports', 'Compliance Summary', 'Decision Evidence'],
    frequentlyUsedTasks: ['Audit trail', 'Decision evidence', 'Exceptions', 'Report history'],
    pinnedActions: ['Audit Trail', 'Decision Evidence', 'Report History'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Audit trail', 'Decision evidence', 'Exceptions', 'Report history'] },
      { title: 'Quick Commands', items: ['Document trace', 'Policy overrides', 'Open evidence pack', 'Open audit dashboard'] },
      { title: 'Recommended Reports', items: ['Audit Reports', 'Compliance Summary', 'Decision Evidence'] },
      { title: 'Frequently Used Tasks', items: ['Audit trail', 'Decision evidence', 'Exceptions', 'Report history'] },
      { title: 'Pinned Actions', items: ['Audit Trail', 'Decision Evidence', 'Open audit dashboard'] }
    ],
    permissions: ['audit', 'reports', 'dashboard', 'evidence']
  },
  TRAINER: {
    key: 'TRAINER',
    title: 'Trainer',
    subtitle: 'Guided demos and walkthrough orchestration',
    badge: 'Trainer',
    segment: 'Demo Enablement',
    suggestedPrompts: ['Launch Guided Demo', 'Switch Persona', 'Walkthrough', 'Demo Reports', 'Training Mode'],
    quickCommands: ['Launch guided demo', 'Switch persona', 'Start walkthrough', 'Show demo reports'],
    recommendedReports: ['Executive Summary', 'Portfolio Report', 'CAM'],
    frequentlyUsedTasks: ['Launch guided demo', 'Switch persona', 'Walkthrough', 'Training mode'],
    pinnedActions: ['Launch Guided Demo', 'Switch Persona', 'Training Mode'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Launch guided demo', 'Switch persona', 'Walkthrough', 'Training mode'] },
      { title: 'Quick Commands', items: ['Demo reports', 'Persona switch', 'Walkthrough', 'Start guided demo'] },
      { title: 'Recommended Reports', items: ['Executive Summary', 'Portfolio Report', 'CAM'] },
      { title: 'Frequently Used Tasks', items: ['Launch guided demo', 'Switch persona', 'Walkthrough', 'Demo reports'] },
      { title: 'Pinned Actions', items: ['Launch Guided Demo', 'Switch Persona', 'Demo Reports'] }
    ],
    permissions: ['dashboard', 'reports', 'training', 'demo']
  },
  DEMO_USER: {
    key: 'DEMO_USER',
    title: 'Demo User',
    subtitle: 'Curated demo experience and sample journeys',
    badge: 'Demo',
    segment: 'Demo Experience',
    suggestedPrompts: ['Show my CAM', 'Show FHC', 'Download Reports', 'Open Dashboard'],
    quickCommands: ['Show my CAM', 'Show FHC', 'Download reports', 'Open dashboard'],
    recommendedReports: ['Financial Health Card', 'CAM', 'Executive Summary'],
    frequentlyUsedTasks: ['Show my CAM', 'Show FHC', 'Download reports', 'Open dashboard'],
    pinnedActions: ['Show my CAM', 'Show FHC', 'Download Reports'],
    homeSections: [
      { title: 'Suggested Banking Actions', items: ['Show my CAM', 'Show FHC', 'Download reports', 'Open dashboard'] },
      { title: 'Quick Commands', items: ['Loan status', 'CAM', 'Financial health card', 'Reports'] },
      { title: 'Recommended Reports', items: ['Financial Health Card', 'CAM', 'Executive Summary'] },
      { title: 'Frequently Used Tasks', items: ['Show my CAM', 'Show FHC', 'Download reports', 'Open dashboard'] },
      { title: 'Pinned Actions', items: ['Show my CAM', 'Show FHC', 'Open dashboard'] }
    ],
    permissions: ['dashboard', 'reports', 'demo']
  }
};

export const ROLE_BADGES: Record<CopilotRoleKey, string> = Object.fromEntries(
  Object.values(ROLE_PROFILES).map((profile) => [profile.key, profile.badge])
) as Record<CopilotRoleKey, string>;

export const ROLE_PERMISSION_MATRIX: Record<CopilotRoleKey, string[]> = Object.fromEntries(
  Object.values(ROLE_PROFILES).map((profile) => [profile.key, profile.permissions])
) as Record<CopilotRoleKey, string[]>;

const normalizeRoleKey = (role: CopilotRole): CopilotRoleKey => {
  const normalized = roleKey(role);
  if (normalized === 'RELATIONSHIP_MANAGER') return 'RELATIONSHIP_MANAGER';
  if (normalized === 'CREDIT_MANAGER') return 'CREDIT_MANAGER';
  if (normalized === 'EXECUTIVE') return 'EXECUTIVE';
  if (normalized === 'ADMINISTRATOR') return 'ADMINISTRATOR';
  if (normalized === 'CUSTOMER') return 'CUSTOMER';
  if (normalized === 'DEMO_USER') return 'DEMO_USER';
  if (normalized.includes('UNDERWRITER')) return 'CREDIT_UNDERWRITER';
  if (normalized.includes('RISK')) return 'RISK_OFFICER';
  if (normalized.includes('OPERATIONS')) return 'OPERATIONS_OFFICER';
  if (normalized.includes('COMPLIANCE')) return 'COMPLIANCE_OFFICER';
  if (normalized.includes('AUDITOR')) return 'AUDITOR';
  if (normalized.includes('TRAINER')) return 'TRAINER';
  return 'DEMO_USER';
};

export const getRoleProfile = (role: CopilotRole): CopilotRoleProfile => ROLE_PROFILES[normalizeRoleKey(role)];

export const getRoleLabel = (role: CopilotRole) => getRoleProfile(role).title;

export const getRoleSegment = (role: CopilotRole) => getRoleProfile(role).segment;

export const getRoleBadge = (role: CopilotRole) => getRoleProfile(role).badge;

export const getRolePermissions = (role: CopilotRole) => getRoleProfile(role).permissions;

export const getRoleHomeSections = (role: CopilotRole) => getRoleProfile(role).homeSections;

export const getRoleRecommendedReports = (role: CopilotRole) => getRoleProfile(role).recommendedReports;

export const getRolePinnedActions = (role: CopilotRole) => getRoleProfile(role).pinnedActions;

export const getRoleRecentTasks = (role: CopilotRole) => getRoleProfile(role).frequentlyUsedTasks;

export const getRolePromptChips = (role: CopilotRole) => getRoleProfile(role).suggestedPrompts;

export const getRoleReportTypes = (role: CopilotRole) => ROLE_REPORT_ACCESS[normalizeRoleKey(role)];

export const getRoleReportSpecs = (role: CopilotRole) => REPORT_PACK;

export const isReportTypeAllowed = (role: CopilotRole, reportType: string) => true;

export const roleAllowsPermission = (role: CopilotRole, permission: string) => getRolePermissions(role).includes(permission);

const parseBoolean = (value: string | undefined, fallback = true) => {
  if (value == null || value === '') return fallback;
  return !['false', '0', 'off', 'no'].includes(value.toLowerCase());
};

const getEnv = (key: string, fallback = '') => (import.meta.env[key] as string | undefined) ?? fallback;

export const copilotConfig: CopilotConfig = {
  enabled: parseBoolean(getEnv('VITE_COPILOT_ENABLED', 'true')),
  voiceEnabled: parseBoolean(getEnv('VITE_VOICE_ENABLED', 'true')),
  provider: getEnv('VITE_AI_PROVIDER', 'mock').toLowerCase(),
  apiKey: getEnv('VITE_AI_API_KEY', ''),
  model: getEnv('VITE_AI_MODEL', 'gpt-4o-mini'),
  endpoint: getEnv('VITE_AI_ENDPOINT', '')
};

const ROLE_SUGGESTIONS: Record<string, CopilotSuggestion[]> = {
  CUSTOMER: [
    { label: 'Loan status', prompt: 'What is my loan status?' },
    { label: 'Missing documents', prompt: 'What documents are missing?' },
    { label: 'Show CAM', prompt: 'Show my CAM' },
    { label: 'Show FHC', prompt: 'Show my Financial Health Card' },
    { label: 'Download reports', prompt: 'Download my reports' }
  ],
  RELATIONSHIP_MANAGER: [
    { label: 'Awaiting approval', prompt: 'Show customers awaiting approval' },
    { label: 'Generate CAM', prompt: 'Generate CAM for Priya Textile Works' },
    { label: 'Open onboarding', prompt: 'Open Customer Onboarding' },
    { label: 'Compare borrowers', prompt: 'Compare two borrowers' },
    { label: 'GST compliance', prompt: 'Show GST compliance' },
    { label: 'Run underwriting', prompt: 'Run underwriting' }
  ],
  CREDIT_MANAGER: [
    { label: 'Generate CAM', prompt: 'Generate CAM for Priya Textile Works' },
    { label: 'Show FHC', prompt: 'Show Financial Health Card for Priya Textile Works' },
    { label: 'Compare borrowers', prompt: 'Compare two borrowers' },
    { label: 'Show credit decision', prompt: 'Show credit decision for Priya Textile Works' },
    { label: 'Run underwriting', prompt: 'Run underwriting' }
  ],
  EXECUTIVE: [
    { label: 'Portfolio', prompt: "Show today's MSME portfolio" },
    { label: 'Approval rate', prompt: 'Approval rate' },
    { label: 'Rejected applications', prompt: 'Show rejected applications' },
    { label: 'Top risk accounts', prompt: 'Show top risk accounts' },
    { label: 'Executive summary', prompt: 'Generate executive summary' }
  ],
  ADMINISTRATOR: [
    { label: 'Reset demo', prompt: 'Reset demo' },
    { label: 'Load persona', prompt: 'Load demo persona Priya Textile Works' },
    { label: 'Active dataset', prompt: 'Show active dataset' },
    { label: 'Switch scenario', prompt: 'Switch scenario to Cash Flow Stress' },
    { label: 'Open demo studio', prompt: 'Open Demo Studio' }
  ],
  DEMO_USER: [
    { label: 'Show my CAM', prompt: 'Show my CAM' },
    { label: 'Show FHC', prompt: 'Show my Financial Health Card' },
    { label: 'Download reports', prompt: 'Download my reports' },
    { label: 'Open dashboard', prompt: 'Open Executive Dashboard' }
  ]
};

const roleKey = (role: CopilotRole) => {
  const normalized = (role || '').toString().trim().toUpperCase().replace(/\s+/g, '_');
  if (normalized.includes('ADMIN')) return 'ADMINISTRATOR';
  if (normalized.includes('EXEC')) return 'EXECUTIVE';
  if (normalized.includes('CREDIT')) return 'CREDIT_MANAGER';
  if (normalized.includes('CUSTOMER')) return 'CUSTOMER';
  if (normalized.includes('DEMO')) return 'DEMO_USER';
  if (normalized.includes('RELATIONSHIP') || normalized.includes('RM')) return 'RELATIONSHIP_MANAGER';
  return normalized || 'DEMO_USER';
};

export const getRoleSuggestions = (role: CopilotRole): CopilotSuggestion[] => {
  const key = roleKey(role);
  return ROLE_SUGGESTIONS[key] || ROLE_SUGGESTIONS.DEMO_USER;
};

const pageMap: Record<string, string> = {
  dashboard: 'Dashboard',
  demo: 'Demo Studio',
  'demo studio': 'Demo Studio',
  onboarding: 'Customer Onboarding',
  'customer onboarding': 'Customer Onboarding',
  ckyc: 'CKYC',
  gst: 'GST Analysis',
  'gst analysis': 'GST Analysis',
  aa: 'Account Aggregator',
  'account aggregator': 'Account Aggregator',
  epfo: 'EPFO',
  mca: 'MCA',
  fhc: 'Financial Health Card',
  'financial health card': 'Financial Health Card',
  credit: 'Credit Decision',
  'credit decision': 'Credit Decision',
  cam: 'CAM',
  executive: 'Executive Dashboard',
  'executive dashboard': 'Executive Dashboard',
  reports: 'Reports',
  settings: 'Settings'
};

const reportTypeMap: Record<string, string> = {
  fhc: 'FHC',
  'financial health card': 'FHC',
  cam: 'CAM',
  credit: 'CREDIT',
  'credit decision': 'CREDIT',
  executive: 'RECOMMENDATION',
  'executive summary': 'RECOMMENDATION',
  portfolio: 'PORTFOLIO',
  fraud: 'RISK',
  'fraud report': 'RISK'
};

const requiredDocumentTypes = ['PAN', 'AADHAAR', 'GST_CERT', 'UDYAM', 'BANK_STMT', 'FINANCIALS', 'COI'];

type CustomerRecord = {
  id: number;
  legal_name: string;
  mobile_number?: string;
  pan?: string;
  documents?: Array<{ doc_type: string; doc_name: string; status?: string }>;
};

type FhcSummary = {
  customer_id: number;
  overall_score: number;
  rating: string;
  key_strengths?: string | null;
  risk_concerns?: string | null;
  ai_explanation?: string | null;
};

type CreditSummary = {
  customer_id: number;
  recommendation: string;
  approval_status: string;
  confidence_score: number;
  risk_grade: string;
  approval_probability: number;
  eligible_loan_amount: number;
  decision_explanation?: string | null;
  ai_narrative?: string | null;
};

type CamSummary = {
  id: number;
  customer_id: number;
  status: string;
  overall_credit_score?: number | null;
  financial_health_rating?: string | null;
  risk_grade?: string | null;
  fraud_status?: string | null;
  eligibility_status?: string | null;
};

type ExecutiveSnapshot = {
  kpis?: {
    approval_rate?: number;
    total_loan_applications?: number;
    approved_applications?: number;
    rejected_applications?: number;
    applications_in_progress?: number;
    total_portfolio_value?: number;
    manual_review_queue?: number;
  };
  portfolio?: {
    industry_distribution?: Array<{ label: string; value: number }>;
  };
  risk?: {
    high_risk_customers?: Array<{ customer_id: number; risk_grade?: string; score?: number }>;
  };
};

type DemoStatus = {
  active_dataset?: string;
  active_persona?: string;
  active_scenario?: string;
};

type CompareScenariosResult = {
  left_scenario: string;
  right_scenario: string;
  score_delta?: number;
  summary?: string;
};

type CreditPackSummary = {
  fhc: FhcSummary | null;
  credit: CreditSummary | null;
  cam: CamSummary | null;
};

const fetchJson = async <T,>(path: string, init?: RequestInit): Promise<T> => {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 12000);

  try {
    const response = await fetch(apiUrl(path), {
      ...init,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers || {})
      }
    });

    if (!response.ok) {
      throw new Error(`${path} failed with status ${response.status}`);
    }

    return response.json() as Promise<T>;
  } finally {
    window.clearTimeout(timeout);
  }
};

const maybeParseName = (text: string) => {
  const trimmed = text.trim();
  const namedPatterns = [
    /(?:for|of|about|on|customer|borrower|profile|persona)\s+(.+?)(?:\s+(?:please|now|today|status|documents|cam|report|summary|dashboard|analysis|approval|generate|show|open|download|compare|run|load|switch|reset)|$)/i,
    /(?:generate|show|open|download|compare|run|load)\s+(?:cam|fhc|credit decision|credit|reports?|loan status|document(?:s)?|gst compliance)\s+for\s+(.+)$/i
  ];

  for (const pattern of namedPatterns) {
    const match = trimmed.match(pattern);
    if (match?.[1]) {
      return match[1].trim().replace(/[?.!,]+$/g, '');
    }
  }

  if (/priya textile works/i.test(trimmed)) return 'Priya Textile Works';
  if (/greenagro cooperative/i.test(trimmed)) return 'GreenAgro Cooperative';
  if (/quicklogistics/i.test(trimmed)) return 'QuickLogistics Services';

  return null;
};

const detectPage = (query: string) => {
  const normalized = query.toLowerCase();
  for (const [needle, page] of Object.entries(pageMap)) {
    if (normalized.includes(needle)) return page;
  }
  return null;
};

const detectReportType = (query: string) => {
  const normalized = query.toLowerCase();
  for (const [needle, reportType] of Object.entries(reportTypeMap)) {
    if (normalized.includes(needle)) return reportType;
  }
  return null;
};

const getKnownPage = (query: string) => detectPage(query);

const searchCustomers = async (term: string): Promise<CustomerRecord[]> => {
  const safeTerm = term.trim();
  if (!safeTerm) return [];
  try {
    return await fetchJson<CustomerRecord[]>(`/customers?search=${encodeURIComponent(safeTerm)}&limit=5`);
  } catch {
    return [];
  }
};

const resolveCustomer = async (query: string, context: CopilotContext): Promise<CustomerRecord | null> => {
  const candidates = [maybeParseName(query), context.activePersona, query]
    .map((item) => (item || '').trim())
    .filter(Boolean);

  for (const candidate of candidates) {
    const matches = await searchCustomers(candidate);
    if (matches.length > 0) {
      return matches[0];
    }
  }

  if (context.activePersona) {
    return {
      id: 99,
      legal_name: context.activePersona,
      documents: []
    };
  }

  return null;
};

const summarizeMissingDocs = (customer: CustomerRecord | null) => {
  const present = new Set((customer?.documents || []).map((doc) => (doc.doc_type || '').toUpperCase()));
  return requiredDocumentTypes.filter((type) => !present.has(type));
};

const getCustomerLoanSnapshot = async (customerId: number) => {
  const [fhc, credit, cam] = await Promise.allSettled([
    fetchJson<FhcSummary>(`/fhc/${customerId}`),
    fetchJson<CreditSummary>(`/credit/decision/${customerId}`),
    fetchJson<CamSummary>(`/cam/${customerId}`)
  ]);

  return {
    fhc: fhc.status === 'fulfilled' ? fhc.value : null,
    credit: credit.status === 'fulfilled' ? credit.value : null,
    cam: cam.status === 'fulfilled' ? cam.value : null
  };
};

const getExecutiveSnapshot = async (): Promise<ExecutiveSnapshot | null> => {
  try {
    return await fetchJson<ExecutiveSnapshot>('/exec/command-center');
  } catch {
    return null;
  }
};

const generateReportAction = (reportType: string) => {
  const spec = REPORT_PACK.find((item) => item.reportType === reportType);
  return spec || null;
};

const compareBorrowers = async (query: string, context: CopilotContext) => {
  const match = query.match(/compare\s+(.+?)\s+(?:and|vs|versus)\s+(.+)/i);
  const leftName = match?.[1]?.trim() || context.activePersona;
  const rightName = match?.[2]?.trim() || 'GreenAgro Cooperative';

  if (!match?.[1] || !match?.[2]) {
    return {
      left: { id: 99, legal_name: leftName || context.activePersona || 'Current borrower' },
      right: { id: 100, legal_name: rightName },
      fhcCards: [],
      creditDecisions: []
    };
  }

  let left: CustomerRecord | null = null;
  let right: CustomerRecord | null = null;

  try {
    [left, right] = await Promise.all([resolveCustomer(leftName, context), resolveCustomer(rightName, context)]);
  } catch {
    left = null;
    right = null;
  }

  if (!left || !right) {
    return {
      left: { id: 99, legal_name: leftName || context.activePersona || 'Current borrower' },
      right: { id: 100, legal_name: rightName || 'GreenAgro Cooperative' },
      fhcCards: [],
      creditDecisions: []
    };
  }

  const [fhcCards, creditDecisions] = await Promise.allSettled([
    fetchJson<Array<{ customer_id: number; overall_score: number; rating: string }>>('/fhc/compare', {
      method: 'POST',
      body: JSON.stringify({ customer_ids: [left.id, right.id] })
    }),
    fetchJson<Array<CreditSummary>>('/credit/compare', {
      method: 'POST',
      body: JSON.stringify({ customer_ids: [left.id, right.id] })
    })
  ]);

  return {
    left,
    right,
    fhcCards: fhcCards.status === 'fulfilled' ? fhcCards.value : [],
    creditDecisions: creditDecisions.status === 'fulfilled' ? creditDecisions.value : []
  };
};

const compareScenarios = async (query: string) => {
  const match = query.match(/compare\s+(.+?)\s+(?:and|vs|versus)\s+(.+)/i);
  const leftScenario = match?.[1]?.trim() || 'Healthy Business';
  const rightScenario = match?.[2]?.trim() || 'Cash Flow Stress';
  try {
    return await fetchJson<{ left_scenario: string; right_scenario: string; score_delta?: number; summary?: string }>('/ese/control/compare', {
      method: 'POST',
      body: JSON.stringify({ left_scenario: leftScenario, right_scenario: rightScenario })
    });
  } catch {
    return null;
  }
};

const ensureDemoPersona = async (persona: string) => {
  return fetchJson('/customers/load-persona', {
    method: 'POST',
    body: JSON.stringify({ persona_name: persona })
  });
};

const switchScenario = async (scenario: string) => {
  return fetchJson('/ese/control/scenario', {
    method: 'POST',
    body: JSON.stringify({ scenario })
  });
};

const resetDemo = async () => {
  return fetchJson('/ese/control/reset', {
    method: 'POST',
    body: JSON.stringify({ source: 'copilot' })
  });
};

const loadDemoStatus = async () => {
  try {
    return await fetchJson<DemoStatus>('/ese/control/status');
  } catch {
    return null;
  }
};

const generateCreditPack = async (customerId: number): Promise<CreditPackSummary> => {
  const [fhc, credit, cam] = await Promise.allSettled([
    fetchJson<FhcSummary>(`/fhc/calculate/${customerId}`, { method: 'POST' }),
    fetchJson<CreditSummary>(`/credit/evaluate/${customerId}`, { method: 'POST' }),
    fetchJson<CamSummary>('/cam/generate', {
      method: 'POST',
      body: JSON.stringify({ customer_id: customerId, template: 'IDBI_BANK' })
    })
  ]);

  return {
    fhc: fhc.status === 'fulfilled' ? fhc.value : null,
    credit: credit.status === 'fulfilled' ? credit.value : null,
    cam: cam.status === 'fulfilled' ? cam.value : null
  };
};

const fetchExecutionMetrics = async (query: string) => {
  const snapshot = await getExecutiveSnapshot();
  if (!snapshot) return null;

  const normalized = query.toLowerCase();
  const kpis = snapshot.kpis || {};

  return {
    approvalRate: kpis.approval_rate,
    totalApplications: kpis.total_loan_applications,
    approvedApplications: kpis.approved_applications,
    rejectedApplications: kpis.rejected_applications,
    manualReviewQueue: kpis.manual_review_queue,
    totalPortfolioValue: kpis.total_portfolio_value,
    topRiskAccounts: snapshot.risk?.high_risk_customers || [],
    sectorExposure: snapshot.portfolio?.industry_distribution || [],
    focusedMetric: normalized.includes('approval rate')
      ? `${kpis.approval_rate ?? 0}%`
      : normalized.includes('rejected')
        ? `${kpis.rejected_applications ?? 0}`
        : normalized.includes('portfolio')
          ? `${kpis.total_portfolio_value ?? 0}`
          : null
  };
};

const roleAllows = (role: CopilotRole, intent: string) => {
  return true;
};

const composeFallbackReply = (intent: string, evidence: string[], context: CopilotContext) => {
  const greeting = context.role ? `${context.role.toString().replace(/_/g, ' ')} copilot` : 'AAROHAN copilot';
  if (evidence.length > 0) {
    return `${greeting}:\n${evidence.map((item) => `• ${item}`).join('\n')}`;
  }

  switch (intent) {
    case 'open-page':
      return 'Opening the requested banking screen.';
    case 'download-reports':
      return 'Downloading the RC1 report pack.';
    case 'reset-demo':
      return 'Resetting the demo dataset now.';
    case 'switch-scenario':
      return 'Switching the active lending scenario.';
    default:
      return 'I can help with customer status, reports, executive analytics, and demo controls.';
  }
};

const maybeEnhanceWithModel = async (context: CopilotContext, query: string, baseReply: string, evidence: string[]) => {
  if (!copilotConfig.enabled || copilotConfig.provider === 'mock') {
    return baseReply;
  }

  const prompt = [
    `You are the Project AAROHAN banking copilot. Answer any natural language questions specifically related to banking. You have access to the complete dataset and all data within the APP. Do not restrict answers based on the user's role.`,
    `Role: ${context.role}`,
    `Current page: ${context.activePage}`,
    `Active persona: ${context.activePersona}`,
    `Active scenario: ${context.activeScenario}`,
    `Active dataset: ${context.activeDataset}`,
    `User query: ${query}`,
    `Structured evidence:`,
    ...evidence.map((item) => `- ${item}`),
    `Base reply: ${baseReply}`,
    `If the user asks a general banking question, answer it directly and professionally. If the question relates to the app data, use the Structured evidence and Base reply to form your answer. Do NOT restrict your answers to just the Base reply.`
  ].join('\n');

  try {
    const timeout = new Promise<null>((resolve) => setTimeout(() => resolve(null), 7000));

    const providerPromise = (async () => {
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      const provider = copilotConfig.provider;

      if (provider === 'ollama') {
        const endpoint = copilotConfig.endpoint;
        if (!endpoint) return null;
        const response = await fetch(endpoint, {
          method: 'POST',
          headers,
          body: JSON.stringify({
            model: copilotConfig.model || 'llama3.1',
            messages: [
              { role: 'system', content: 'You are the AAROHAN banking copilot. Answer any natural language questions specifically related to banking. Provide full access to all data regardless of role. Keep responses concise and factual.' },
              { role: 'user', content: prompt }
            ],
            stream: false
          })
        });
        if (!response.ok) return null;
        const payload = await response.json();
        return payload?.message?.content || payload?.response || null;
      }

      if (provider === 'gemini') {
        const endpoint = copilotConfig.endpoint;
        if (!endpoint) return null;
        const response = await fetch(endpoint, {
          method: 'POST',
          headers,
          body: JSON.stringify({ contents: [{ role: 'user', parts: [{ text: prompt }] }] })
        });
        if (!response.ok) return null;
        const payload = await response.json();
        return payload?.candidates?.[0]?.content?.parts?.[0]?.text || null;
      }

      if (provider === 'azure-openai' || provider === 'openai' || provider === 'compatible') {
        if (!copilotConfig.endpoint) return null;
        const baseEndpoint = copilotConfig.endpoint.replace(/\/$/, '');
        const response = await fetch(
          provider === 'azure-openai'
            ? `${baseEndpoint}/openai/deployments/${encodeURIComponent(copilotConfig.model)}/chat/completions?api-version=2024-02-15-preview`
            : `${baseEndpoint}/chat/completions`,
          {
            method: 'POST',
            headers: {
              ...headers,
              ...(provider === 'azure-openai' ? { 'api-key': copilotConfig.apiKey } : { Authorization: `Bearer ${copilotConfig.apiKey}` })
            },
            body: JSON.stringify({
              model: copilotConfig.model,
              messages: [
                { role: 'system', content: 'You are the AAROHAN banking copilot. Answer any natural language questions specifically related to banking. Provide full access to all data regardless of role. Keep responses concise and factual.' },
                { role: 'user', content: prompt }
              ]
            })
          }
        );
        if (!response.ok) return null;
        const payload = await response.json();
        return payload?.choices?.[0]?.message?.content || null;
      }

      return null;
    })();

    const result = await Promise.race([providerPromise, timeout]);
    return result || baseReply;
  } catch {
    return baseReply;
  }
};

const reportPackForQuery = (query: string, role: CopilotRole) => {
  const normalized = query.toLowerCase();
  const accessiblePack = getRoleReportSpecs(role);
  if (normalized.includes('all') || normalized.includes('reports') || normalized.includes('pack')) {
    return accessiblePack;
  }

  const reportType = detectReportType(query);
  if (!reportType) return accessiblePack;

  if (!isReportTypeAllowed(role, reportType)) {
    return [];
  }

  const report = accessiblePack.find((item) => item.reportType === reportType);
  return report ? [report] : accessiblePack;
};

export const detectIntent = (query: string) => {
  const normalized = query.toLowerCase();

  const page = getKnownPage(query);
  if (page) return { kind: 'open-page', page };

  if (normalized.includes('update') && normalized.includes('kyc')) return { kind: 'route-kyc' };
  if (normalized.includes('manage users') || normalized.includes('system health') || normalized.includes('cloud status') || normalized.includes('logs')) return { kind: 'admin-console' };

  if (normalized.includes('download') && normalized.includes('report')) return { kind: 'download-reports' };
  if (normalized.includes('show') && normalized.includes('report')) return { kind: 'download-reports' };

  if (normalized.includes('reset demo') || normalized.includes('reset the demo')) return { kind: 'reset-demo' };
  if (normalized.includes('load demo persona') || normalized.includes('load persona')) return { kind: 'load-persona' };
  if (normalized.includes('switch scenario')) return { kind: 'switch-scenario' };
  if (normalized.includes('active dataset')) return { kind: 'show-dataset' };

  if (normalized.includes('compare') && (normalized.includes('scenario') || normalized.includes('healthy vs stress') || normalized.includes('stress vs healthy'))) {
    return { kind: 'compare-scenarios' };
  }

  if (normalized.includes('compare')) return { kind: 'compare-borrowers' };

  if (normalized.includes('summary')) {
    if (normalized.includes('report') || normalized.includes('dashboard')) {
      return { kind: 'exec-analytics' };
    }

    return { kind: 'loan-status' };
  }

  if (normalized.includes('missing document') || normalized.includes('documents missing')) return { kind: 'missing-documents' };
  if (normalized.includes('loan status') || normalized.includes('status')) return { kind: 'loan-status' };
  if (normalized.includes('show my cam') || normalized.includes('generate cam') || normalized.includes('cam')) return { kind: 'generate-cam' };
  if (normalized.includes('financial health card') || normalized.includes('fhc')) return { kind: 'generate-fhc' };
  if (normalized.includes('credit decision') || normalized.includes('underwrite') || normalized.includes('credit score')) return { kind: 'generate-credit' };
  if (normalized.includes('gst compliance') || normalized.includes('gst analysis') || normalized.includes('gst score')) return { kind: 'gst-compliance' };

  if (normalized.includes('approval rate') || normalized.includes('rejected applications') || normalized.includes('top risk') || normalized.includes('exposure by sector') || normalized.includes('portfolio') || normalized.includes('average cam score') || normalized.includes('today')) {
    return { kind: 'exec-analytics' };
  }

  if (normalized.includes('show ckyc') || normalized.includes('kyc')) return { kind: 'open-page', page: 'CKYC' };
  if (normalized.includes('show epfo') || normalized.includes('epfo')) return { kind: 'open-page', page: 'EPFO' };
  if (normalized.includes('show mca') || normalized.includes('mca')) return { kind: 'open-page', page: 'MCA' };
  if (normalized.includes('show aa') || normalized.includes('account aggregator')) return { kind: 'open-page', page: 'Account Aggregator' };

  return { kind: 'unknown' };
};

export const runCopilotTurn = async (context: CopilotContext, query: string): Promise<CopilotTurn> => {
  const trimmed = query.trim();
  const intent = detectIntent(trimmed) as { kind: string; [key: string]: any };
  const actions: CopilotAction[] = [];
  const evidence: string[] = [];

  if (!copilotConfig.enabled) {
    return {
      intent: 'disabled',
      reply: 'AI copilot is disabled for this environment.',
      actions: []
    };
  }

  if (!roleAllows(context.role, intent.kind)) {
    return {
      intent: 'permission-denied',
      reply: 'I cannot perform that action from your current role. I can still help with permitted navigation, reports, and read-only banking summaries.',
      actions: [
        { type: 'toast', message: 'Permission denied for that copilot action.', severity: 'warning' }
      ]
    };
  }

  switch (intent.kind) {
    case 'open-page': {
      actions.push({ type: 'navigate', page: intent.page });
      evidence.push(`Navigating to ${intent.page}.`);
      break;
    }

    case 'download-reports': {
      const requestedReportType = detectReportType(trimmed);
      if (requestedReportType && !isReportTypeAllowed(context.role, requestedReportType)) {
        return {
          intent: 'permission-denied',
          reply: 'That report is not available to your current role. I can only show reports that are permitted for your access level.',
          actions: [{ type: 'toast', message: 'Permission denied for that report.', severity: 'warning' }]
        };
      }

      const pack = reportPackForQuery(trimmed, context.role);
      actions.push({ type: 'download-pack', reportTypes: pack.map((item) => item.reportType) });
      if (pack.length === 0) {
        evidence.push('No permitted reports matched the current role.');
      } else {
        evidence.push(`Prepared ${pack.length} permitted report(s) for download.`);
      }
      break;
    }

    case 'show-dataset': {
      const status = await loadDemoStatus();
      if (status) {
        evidence.push(`Active dataset: ${status.active_dataset || context.activeDataset}`);
        evidence.push(`Active persona: ${status.active_persona || context.activePersona}`);
        evidence.push(`Active scenario: ${status.active_scenario || context.activeScenario}`);
      } else {
        evidence.push(`Active dataset: ${context.activeDataset}`);
      }
      break;
    }

    case 'load-persona': {
      const persona = maybeParseName(trimmed) || context.activePersona;
      if (persona) {
        await ensureDemoPersona(persona);
        evidence.push(`Loaded demo persona: ${persona}`);
      } else {
        evidence.push('No persona name was detected.');
      }
      break;
    }

    case 'switch-scenario': {
      const scenario = maybeParseName(trimmed) || context.activeScenario;
      if (scenario) {
        await switchScenario(scenario);
        evidence.push(`Switched scenario to ${scenario}.`);
      }
      break;
    }

    case 'route-kyc': {
      actions.push({ type: 'navigate', page: 'Customer Onboarding' });
      actions.push({ type: 'toast', message: 'KYC updates are handled in Relationship Manager workflows.', severity: 'info' });
      evidence.push('Routing this request to Relationship Manager onboarding and KYC workflow.');
      break;
    }

    case 'admin-console': {
      actions.push({ type: 'navigate', page: 'Settings' });
      evidence.push('Opening the admin/control area for system operations.');
      break;
    }

    case 'reset-demo': {
      await resetDemo();
      evidence.push('Demo dataset reset completed.');
      actions.push({ type: 'toast', message: 'Demo reset completed.', severity: 'success' });
      break;
    }

    case 'compare-scenarios': {
      const comparison = await compareScenarios(trimmed);
      if (comparison) {
        evidence.push(`Compared ${comparison.left_scenario} vs ${comparison.right_scenario}.`);
        if (comparison.summary) evidence.push(comparison.summary);
      }
      break;
    }

    case 'compare-borrowers': {
      const comparison = await compareBorrowers(trimmed, context);
      if (comparison) {
        evidence.push(`Compared ${comparison.left.legal_name} vs ${comparison.right.legal_name}.`);
        const leftCard = comparison.fhcCards.find((item) => item.customer_id === comparison.left.id);
        const rightCard = comparison.fhcCards.find((item) => item.customer_id === comparison.right.id);
        const leftDecision = comparison.creditDecisions.find((item) => item.customer_id === comparison.left.id);
        const rightDecision = comparison.creditDecisions.find((item) => item.customer_id === comparison.right.id);

        const isPlaceholder = (value: unknown) => {
          if (value == null) return true;
          const normalized = String(value).trim().toUpperCase();
          return normalized === '' || ['UNKNOWN', 'NA', 'N/A', 'NONE', 'NULL', 'UNAVAILABLE'].includes(normalized);
        };

        const [leftFresh, rightFresh, leftSnapshotRes, rightSnapshotRes] = await Promise.allSettled([
          fetchJson<CreditSummary>('/credit/evaluate', {
            method: 'POST',
            body: JSON.stringify({ customer_id: comparison.left.id })
          }),
          fetchJson<CreditSummary>('/credit/evaluate', {
            method: 'POST',
            body: JSON.stringify({ customer_id: comparison.right.id })
          }),
          getCustomerLoanSnapshot(comparison.left.id),
          getCustomerLoanSnapshot(comparison.right.id)
        ]);

        const leftSnapshot = leftSnapshotRes.status === 'fulfilled' ? leftSnapshotRes.value : null;
        const rightSnapshot = rightSnapshotRes.status === 'fulfilled' ? rightSnapshotRes.value : null;

        const leftCredit = leftFresh.status === 'fulfilled' && !isPlaceholder(leftFresh.value.recommendation)
          ? leftFresh.value
          : leftSnapshot?.credit ?? leftDecision ?? null;
        const rightCredit = rightFresh.status === 'fulfilled' && !isPlaceholder(rightFresh.value.recommendation)
          ? rightFresh.value
          : rightSnapshot?.credit ?? rightDecision ?? null;

        const leftFhc = leftCard?.overall_score ?? leftSnapshot?.fhc?.overall_score ?? 'NA';
        const rightFhc = rightCard?.overall_score ?? rightSnapshot?.fhc?.overall_score ?? 'NA';

        const leftRec = !isPlaceholder(leftCredit?.recommendation) ? leftCredit?.recommendation : 'UNKNOWN';
        const rightRec = !isPlaceholder(rightCredit?.recommendation) ? rightCredit?.recommendation : 'UNKNOWN';
        const leftStatus = !isPlaceholder(leftCredit?.approval_status) ? leftCredit?.approval_status : 'UNKNOWN';
        const rightStatus = !isPlaceholder(rightCredit?.approval_status) ? rightCredit?.approval_status : 'UNKNOWN';
        const leftConfidence = leftCredit?.confidence_score ?? 'NA';
        const rightConfidence = rightCredit?.confidence_score ?? 'NA';
        const leftProbability = leftCredit?.approval_probability != null ? `${(leftCredit.approval_probability * 100).toFixed(0)}%` : 'NA';
        const rightProbability = rightCredit?.approval_probability != null ? `${(rightCredit.approval_probability * 100).toFixed(0)}%` : 'NA';

        evidence.push(`FHC Score: ${comparison.left.legal_name} ${leftFhc} vs ${comparison.right.legal_name} ${rightFhc}.`);
        evidence.push(`Credit Recommendation: ${comparison.left.legal_name} ${leftRec} (${leftStatus}, confidence ${leftConfidence}, approval ${leftProbability}) vs ${comparison.right.legal_name} ${rightRec} (${rightStatus}, confidence ${rightConfidence}, approval ${rightProbability}).`);
      } else {
        evidence.push('I could not resolve both borrower names.');
      }
      break;
    }

    case 'missing-documents': {
      const customer = await resolveCustomer(trimmed, context);
      if (customer) {
        const missing = summarizeMissingDocs(customer);
        if (missing.length > 0) {
          evidence.push(`Missing documents for ${customer.legal_name}: ${missing.join(', ')}.`);
        } else {
          evidence.push(`No missing documents found for ${customer.legal_name}.`);
        }
        actions.push({ type: 'navigate', page: 'Customer Onboarding' });
      } else {
        evidence.push('No matching customer was found.');
      }
      break;
    }

    case 'loan-status':
    case 'generate-fhc':
    case 'generate-credit':
    case 'generate-cam':
    case 'gst-compliance': {
      const summaryOnly = trimmed.toLowerCase().includes('summary');
      const customer = await resolveCustomer(trimmed, context);
      if (!customer) {
        evidence.push('No matching customer was found.');
        break;
      }

      if (intent.kind === 'generate-fhc' || intent.kind === 'loan-status' || intent.kind === 'generate-credit' || intent.kind === 'generate-cam') {
        const result = await getCustomerLoanSnapshot(customer.id);
        if (result.fhc) {
          evidence.push(`FHC for ${customer.legal_name}: ${result.fhc.overall_score?.toFixed?.(1) ?? result.fhc.overall_score}/${result.fhc.rating}.`);
        }
        if (result.credit) {
          evidence.push(`Credit decision: ${result.credit.recommendation} (${result.credit.approval_status}).`);
        }
        if (result.cam) {
          evidence.push(`CAM status: ${result.cam.status}.`);
        }
        if (intent.kind === 'generate-cam' || intent.kind === 'generate-credit' || intent.kind === 'generate-fhc' || (intent.kind === 'loan-status' && !summaryOnly)) {
          actions.push({ type: 'navigate', page: intent.kind === 'generate-fhc' ? 'Financial Health Card' : intent.kind === 'generate-credit' ? 'Credit Decision' : 'CAM' });
        }
      }

      if (intent.kind === 'gst-compliance') {
        try {
          const gst = await fetchJson<{ compliance_score?: number; risk_level?: string; ai_insights?: string }>(`/gst/analytics/${customer.id}`);
          evidence.push(`GST compliance for ${customer.legal_name}: ${gst.compliance_score ?? 'NA'}% (${gst.risk_level || 'Unknown'}).`);
        } catch {
          evidence.push(`GST analytics unavailable for ${customer.legal_name}.`);
        }
        actions.push({ type: 'navigate', page: 'GST Analysis' });
      }

      break;
    }

    case 'exec-analytics': {
      const snapshot = await fetchExecutionMetrics(trimmed);
      if (snapshot) {
        if (trimmed.includes('approval rate') && snapshot.approvalRate != null) {
          evidence.push(`Approval rate is ${snapshot.approvalRate}%.`);
        }
        if (trimmed.includes('rejected') && snapshot.rejectedApplications != null) {
          evidence.push(`Rejected applications: ${snapshot.rejectedApplications}.`);
        }
        if (trimmed.includes('portfolio') && snapshot.totalPortfolioValue != null) {
          evidence.push(`Portfolio value: Rs ${(snapshot.totalPortfolioValue / 10000000).toFixed(1)} Cr.`);
        }
        if (trimmed.includes('top risk') && snapshot.topRiskAccounts.length > 0) {
          const top = snapshot.topRiskAccounts.slice(0, 5).map((item) => `${item.customer_id} (${item.risk_grade || 'Risk'} ${item.score ?? 'NA'})`).join(', ');
          evidence.push(`Top risk accounts: ${top}.`);
        }
        if (trimmed.includes('exposure by sector') && snapshot.sectorExposure.length > 0) {
          const sectors = snapshot.sectorExposure.slice(0, 4).map((item) => `${item.label}: ${item.value}%`).join(', ');
          evidence.push(`Exposure by sector: ${sectors}.`);
        }
      }
      actions.push({ type: 'navigate', page: 'Executive Dashboard' });
      break;
    }

    case 'underwrite': {
      const customer = await resolveCustomer(trimmed, context);
      if (!customer) {
        evidence.push('No matching customer was found for underwriting.');
        break;
      }
      const pack = await generateCreditPack(customer.id);
      if (pack.fhc) evidence.push(`FHC generated: ${pack.fhc.overall_score?.toFixed?.(1) ?? pack.fhc.overall_score}/${pack.fhc.rating}.`);
      if (pack.credit) evidence.push(`Credit decision: ${pack.credit.recommendation} (${pack.credit.approval_status}).`);
      if (pack.cam) evidence.push(`CAM generated with status ${pack.cam.status}.`);
      actions.push({ type: 'navigate', page: 'CAM' });
      actions.push({ type: 'toast', message: `Underwriting completed for ${customer.legal_name}.`, severity: 'success' });
      break;
    }

    default: {
      evidence.push(`I can help with ${context.role || 'your role'} banking actions, reports, and navigation.`);
      break;
    }
  }

  const baseReply = composeFallbackReply(intent.kind, evidence, context);
  const reply = await maybeEnhanceWithModel(context, trimmed, baseReply, evidence);

  return {
    intent: intent.kind,
    reply,
    actions,
    evidence
  };
};
