import React from 'react';
import {
  Alert,
  Box,
  Button,
  Chip,
  Divider,
  Drawer,
  Fab,
  IconButton,
  InputAdornment,
  LinearProgress,
  Paper,
  Stack,
  TextField,
  Tooltip,
  Typography,
  useMediaQuery,
  useTheme
} from '@mui/material';
import {
  AutoAwesome,
  Close,
  Download,
  Mic,
  MicOff,
  Send,
  SmartToy,
  VolumeOff,
  VolumeUp,
  History,
  OpenInNew
} from '@mui/icons-material';
import { apiUrl } from '../lib/api';
import { downloadTextFile } from '../lib/download';
import {
  CopilotAction,
  CopilotContext,
  CopilotSuggestion,
  copilotConfig,
  getRoleBadge,
  getRoleHomeSections,
  getRoleLabel,
  getRolePinnedActions,
  getRolePermissions,
  getRoleProfile,
  getRolePromptChips,
  getRoleRecentTasks,
  getRoleRecommendedReports,
  getRoleReportSpecs,
  getRoleSuggestions,
  isReportTypeAllowed,
  runCopilotTurn
} from '../lib/copilot';

type CopilotMessage = {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  timestamp: string;
  intent?: string;
  actions?: CopilotAction[];
};

type Props = {
  isAuthenticated: boolean;
  role: string;
  activePage: string;
  activePersona: string;
  activeScenario: string;
  activeDataset: string;
  userName?: string;
  onNavigate: (page: string) => void;
  onNotify: (message: string, severity?: 'success' | 'info' | 'warning' | 'error') => void;
};

const buildStorageKey = (role: string, persona: string, dataset: string) =>
  `aarohan.copilot.history.v2:${role.trim().toUpperCase().replace(/\s+/g, '_')}:${persona || 'none'}:${dataset || 'none'}`;

const formatTime = (value: string) => new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const buildPromptText = (message: string) => message.trim();

const pause = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const AiBankingCopilotPanel: React.FC<Props> = ({
  isAuthenticated,
  role,
  activePage,
  activePersona,
  activeScenario,
  activeDataset,
  userName,
  onNavigate,
  onNotify
}) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [open, setOpen] = React.useState(false);
  const [draft, setDraft] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [listening, setListening] = React.useState(false);
  const [voiceOptIn, setVoiceOptIn] = React.useState(false);
  const [messages, setMessages] = React.useState<CopilotMessage[]>([]);
  const [ready, setReady] = React.useState(false);
  const [voiceSupported, setVoiceSupported] = React.useState(false);
  const inputRef = React.useRef<HTMLInputElement | null>(null);
  const messagesEndRef = React.useRef<HTMLDivElement | null>(null);
  const recognitionRef = React.useRef<any>(null);
  const roleProfile = React.useMemo(() => getRoleProfile(role), [role]);
  const roleStorageKey = React.useMemo(() => buildStorageKey(role, activePersona, activeDataset), [activeDataset, activePersona, role]);
  const voiceStorageKey = React.useMemo(() => `${roleStorageKey}:voice`, [roleStorageKey]);
  const homeSections = React.useMemo(() => getRoleHomeSections(role), [role]);
  const promptChips = React.useMemo(() => getRolePromptChips(role), [role]);
  const recentTasks = React.useMemo(() => getRoleRecentTasks(role), [role]);
  const pinnedActions = React.useMemo(() => getRolePinnedActions(role), [role]);
  const reportSpecs = React.useMemo(() => getRoleReportSpecs(role), [role]);
  const recommendedReports = React.useMemo(() => getRoleRecommendedReports(role), [role]);
  const permissions = React.useMemo(() => getRolePermissions(role), [role]);
  const speechWindow = window as Window & {
    SpeechRecognition?: new () => any;
    webkitSpeechRecognition?: new () => any;
    speechSynthesis?: SpeechSynthesis;
  };

  const context: CopilotContext = React.useMemo(() => ({
    role,
    activePage,
    activePersona,
    activeScenario,
    activeDataset,
    userName
  }), [activeDataset, activePage, activePersona, activeScenario, role, userName]);

  const suggestions: CopilotSuggestion[] = React.useMemo(() => getRoleSuggestions(role), [role]);

  React.useEffect(() => {
    if (!isAuthenticated || !copilotConfig.enabled) return;
    try {
      const stored = window.localStorage.getItem(roleStorageKey);
      if (stored) {
        const parsed = JSON.parse(stored) as CopilotMessage[];
        if (Array.isArray(parsed) && parsed.length > 0) {
          setMessages(parsed.slice(-20));
        }
      }
      const storedVoice = window.localStorage.getItem(voiceStorageKey);
      if (storedVoice != null) {
        setVoiceOptIn(storedVoice === 'true');
      }
    } catch {
      // ignore storage issues
    } finally {
      setReady(true);
    }
  }, [isAuthenticated, roleStorageKey, voiceStorageKey]);

  React.useEffect(() => {
    if (!ready) return;
    try {
      window.localStorage.setItem(roleStorageKey, JSON.stringify(messages.slice(-20)));
    } catch {
      // ignore storage issues
    }
  }, [messages, ready, roleStorageKey]);

  React.useEffect(() => {
    if (!ready) return;
    try {
      window.localStorage.setItem(voiceStorageKey, String(voiceOptIn));
    } catch {
      // ignore storage issues
    }
  }, [ready, voiceOptIn, voiceStorageKey]);

  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, open]);

  React.useEffect(() => {
    if (!copilotConfig.enabled) return;
    setVoiceSupported(Boolean(speechWindow.SpeechRecognition || speechWindow.webkitSpeechRecognition));
  }, []);

  React.useEffect(() => {
    if (open && messages.length === 0) {
      setMessages([
        {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          text: `How can I help you today? I’m configured for ${roleProfile.title}, ${roleProfile.segment}, and ${roleProfile.subtitle.toLowerCase()}.`,
          timestamp: new Date().toISOString()
        }
      ]);
    }
  }, [messages.length, open, roleProfile]);

  React.useEffect(() => {
    if (!open) {
      setListening(false);
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch {
          // ignore
        }
      }
    } else {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [open]);

  React.useEffect(() => {
    if (copilotConfig.voiceEnabled && voiceSupported && voiceOptIn) return;
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {
        // ignore
      }
    }
    setListening(false);
    if (speechWindow.speechSynthesis) {
      try {
        speechWindow.speechSynthesis.cancel();
      } catch {
        // ignore
      }
    }
  }, [copilotConfig.voiceEnabled, speechWindow.speechSynthesis, voiceOptIn, voiceSupported]);

  const appendMessage = (message: CopilotMessage) => {
    setMessages((prev) => [...prev, message].slice(-20));
  };

  const voiceAvailable = copilotConfig.voiceEnabled && voiceSupported;
  const voiceActive = voiceAvailable && voiceOptIn;

  const speak = (text: string) => {
    if (!voiceActive || !speechWindow.speechSynthesis) return;
    try {
      speechWindow.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.lang = 'en-IN';
      speechWindow.speechSynthesis.speak(utterance);
    } catch {
      // ignore TTS failures
    }
  };

  const downloadReport = async (reportType: string) => {
    if (!isReportTypeAllowed(role, reportType)) {
      throw new Error('That report is not available to your current role.');
    }

    const spec = reportSpecs.find((item) => item.reportType === reportType);
    if (!spec) return;

    const response = await fetch(apiUrl('/ese/control/report'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        report_type: spec.reportType,
        format_type: 'MARKDOWN',
        data: {
          customer_id: 99,
          persona: activePersona,
          scenario: activeScenario,
          dataset: activeDataset,
          active_page: activePage,
          release: 'AAR-AI-026'
        }
      })
    });

    if (!response.ok) {
      throw new Error(`${spec.label} report failed with status ${response.status}`);
    }

    const payload = await response.json();
    const content = typeof payload.content === 'string'
      ? payload.content
      : `# Project AAROHAN - ${spec.label}\n\nGenerated by the AI Banking Copilot.`;

    downloadTextFile(spec.fileName, content, 'text/markdown');
  };

  const executeActions = async (actions: CopilotAction[] = []) => {
    for (const action of actions) {
      if (action.type === 'navigate') {
        onNavigate(action.page);
        onNotify(`Opened ${action.page}.`, 'info');
      }

      if (action.type === 'download-report') {
        await downloadReport(action.reportType);
        onNotify('Report downloaded.', 'success');
      }

      if (action.type === 'download-pack') {
        for (const reportType of action.reportTypes) {
          await downloadReport(reportType);
          await pause(80);
        }
        onNotify('Report pack downloaded.', 'success');
      }

      if (action.type === 'toast') {
        onNotify(action.message, action.severity || 'info');
      }
    }
  };

  const submitPrompt = async (value?: string) => {
    const prompt = buildPromptText(value || draft);
    if (!prompt || loading || !copilotConfig.enabled) return;

    const userMessage: CopilotMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      text: prompt,
      timestamp: new Date().toISOString()
    };

    appendMessage(userMessage);
    setDraft('');
    setLoading(true);

    try {
      const turn = await runCopilotTurn(context, prompt);
      appendMessage({
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        text: turn.reply,
        timestamp: new Date().toISOString(),
        intent: turn.intent,
        actions: turn.actions
      });
      await executeActions(turn.actions);
      speak(turn.reply);
    } catch (exc: any) {
      const message = exc?.message || 'The copilot could not complete that request.';
      appendMessage({
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        text: message,
        timestamp: new Date().toISOString()
      });
      onNotify(message, 'warning');
    } finally {
      setLoading(false);
    }
  };

  const startVoiceCapture = () => {
    const ctor = speechWindow.SpeechRecognition || speechWindow.webkitSpeechRecognition;
    if (!voiceActive || !ctor) {
      onNotify('Voice input is unavailable in this browser. Falling back to text.', 'warning');
      return;
    }

    if (listening && recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {
        // ignore
      }
      setListening(false);
      return;
    }

    const recognition = new ctor();
    recognition.lang = 'en-IN';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognitionRef.current = recognition;
    setListening(true);

    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0]?.transcript || '')
        .join(' ')
        .trim();

      if (transcript) {
        setDraft(transcript);
        submitPrompt(transcript);
      }
    };

    recognition.onerror = (event: any) => {
      onNotify(event?.error ? `Voice input error: ${event.error}` : 'Voice input failed.', 'warning');
      setListening(false);
    };

    recognition.onend = () => setListening(false);

    try {
      recognition.start();
    } catch {
      setListening(false);
      onNotify('Voice input could not start in this browser.', 'warning');
    }
  };

  if (!isAuthenticated || !copilotConfig.enabled) {
    return null;
  }

  return (
    <>
      <Fab
        color="primary"
        variant="extended"
        onClick={() => setOpen(true)}
        sx={{
          position: 'fixed',
          right: 24,
          bottom: 24,
          zIndex: (theme) => theme.zIndex.drawer + 10,
          boxShadow: '0 14px 40px rgba(66,133,244,0.35)'
        }}
      >
        <AutoAwesome sx={{ mr: 1 }} />
        AI Copilot
      </Fab>

      <Drawer
        anchor="right"
        open={open}
        onClose={() => setOpen(false)}
        PaperProps={{
          sx: {
            width: { xs: '100vw', sm: 420, md: 460 },
            maxWidth: '100vw',
            bgcolor: '#07111f',
            color: 'text.primary',
            backgroundImage: 'linear-gradient(180deg, rgba(66,133,244,0.14) 0%, rgba(7,17,31,1) 28%)'
          }
        }}
      >
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          <Box sx={{ p: 2, borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
            <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={1}>
              <Stack direction="row" spacing={1.25} alignItems="center">
                <Box sx={{ width: 38, height: 38, borderRadius: '50%', bgcolor: 'primary.main', display: 'grid', placeItems: 'center' }}>
                  <SmartToy />
                </Box>
                <Box>
                  <Typography variant="subtitle1" fontWeight="bold">AI Banking Copilot</Typography>
                  <Typography variant="caption" color="text.secondary">Role-aware assistant for banking workflows</Typography>
                </Box>
              </Stack>
              <IconButton onClick={() => setOpen(false)} color="inherit">
                <Close />
              </IconButton>
            </Stack>

            <Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mt: 1.5 }}>
              <Chip size="small" label={role.replace(/_/g, ' ')} color="secondary" variant="outlined" />
              <Chip size="small" label={activeDataset.toUpperCase()} variant="outlined" />
              <Chip size="small" label={copilotConfig.provider.toUpperCase()} variant="outlined" />
              {copilotConfig.voiceEnabled && (
                <Chip
                  size="small"
                  label={voiceActive ? 'Voice on' : 'Voice off'}
                  color={voiceActive ? 'success' : 'default'}
                  variant="outlined"
                />
              )}
            </Stack>

            <Stack direction="row" spacing={1} sx={{ mt: 1.5 }}>
              <Tooltip title={voiceAvailable ? (voiceOptIn ? 'Disable voice assistant' : 'Enable voice assistant') : 'Voice unavailable in this browser'}>
                <IconButton
                  size="small"
                  onClick={() => setVoiceOptIn((value) => !value)}
                  disabled={!voiceAvailable}
                  color={voiceOptIn ? 'primary' : 'inherit'}
                >
                  {voiceOptIn ? <VolumeUp fontSize="small" /> : <VolumeOff fontSize="small" />}
                </IconButton>
              </Tooltip>
              <Tooltip title={voiceActive ? 'Speak a query' : 'Enable voice assistant first'}>
                <span>
                  <IconButton size="small" onClick={startVoiceCapture} disabled={!voiceActive} color={listening ? 'primary' : 'inherit'}>
                    {listening ? <MicOff fontSize="small" /> : <Mic fontSize="small" />}
                  </IconButton>
                </span>
              </Tooltip>
              <Button size="small" variant="outlined" startIcon={<History />} onClick={() => {
                setMessages([]);
                onNotify('Conversation cleared.', 'info');
              }}>
                Clear
              </Button>
            </Stack>
          </Box>

          {loading && <LinearProgress />}

          <Box sx={{ p: 2, flexGrow: 1, overflowY: 'auto' }}>
            <Stack spacing={2}>
              <Paper sx={{ p: 2, border: '1px solid rgba(255,255,255,0.08)', bgcolor: 'rgba(255,255,255,0.03)' }}>
                <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 0.5 }}>
                  How can I help you today?
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5 }}>
                  {getRoleLabel(role)} | {roleProfile.segment} | {roleProfile.subtitle}
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ mb: 1.5 }}>
                  <Chip size="small" label={`Role badge: ${getRoleBadge(role)}`} color="secondary" variant="outlined" />
                  <Chip size="small" label={`Permission badge: ${permissions.length} capabilities`} variant="outlined" />
                  <Chip size="small" label={activeDataset.toUpperCase()} variant="outlined" />
                  <Chip size="small" label={activePersona} variant="outlined" />
                </Stack>

                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.75, textTransform: 'uppercase', letterSpacing: 0.6 }}>
                  Suggested prompts
                </Typography>
                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{ mb: 1.25 }}>
                  {promptChips.slice(0, 4).map((item) => (
                    <Chip key={item} size="small" label={item} variant="outlined" />
                  ))}
                </Stack>

                <Stack spacing={1.5}>
                  {homeSections.map((section) => (
                    <Box key={section.title} sx={{ p: 1.25, borderRadius: 1.5, bgcolor: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.04)' }}>
                      <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.75, textTransform: 'uppercase', letterSpacing: 0.6 }}>
                        {section.title}
                      </Typography>
                      <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
                        {section.items.slice(0, 4).map((item) => (
                          <Chip key={`${section.title}-${item}`} size="small" label={item} variant="outlined" />
                        ))}
                      </Stack>
                    </Box>
                  ))}
                </Stack>

                <Divider sx={{ my: 1.5 }} />

                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.75, textTransform: 'uppercase', letterSpacing: 0.6 }}>
                  Accessible reports
                </Typography>
                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
                  {reportSpecs.map((spec) => (
                    <Chip key={spec.reportType} size="small" label={spec.label} color="primary" variant="outlined" />
                  ))}
                </Stack>

                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1.25, mb: 0.75, textTransform: 'uppercase', letterSpacing: 0.6 }}>
                  Frequent tasks
                </Typography>
                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{ mb: 1.25 }}>
                  {recentTasks.slice(0, 3).map((item) => (
                    <Chip key={item} size="small" label={item} variant="outlined" />
                  ))}
                </Stack>

                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.75, textTransform: 'uppercase', letterSpacing: 0.6 }}>
                  Pinned actions
                </Typography>
                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
                  {pinnedActions.slice(0, 3).map((item) => (
                    <Chip key={item} size="small" label={item} color="secondary" variant="outlined" />
                  ))}
                </Stack>

                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1.25, mb: 0.75, textTransform: 'uppercase', letterSpacing: 0.6 }}>
                  Recommended reports
                </Typography>
                <Typography variant="body2" sx={{ lineHeight: 1.45 }}>
                  {recommendedReports.join(' · ')}
                </Typography>

                {messages.length > 0 && (
                  <>
                    <Divider sx={{ my: 1.5 }} />
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.75, textTransform: 'uppercase', letterSpacing: 0.6 }}>
                      Recent conversations
                    </Typography>
                    <Stack spacing={0.75}>
                      {messages.slice(-4).map((message) => (
                        <Box key={message.id} sx={{ p: 1, borderRadius: 1.25, bgcolor: 'rgba(255,255,255,0.02)' }}>
                          <Typography variant="caption" color="text.secondary">
                            {message.role === 'user' ? 'You' : 'Copilot'} · {formatTime(message.timestamp)}
                          </Typography>
                          <Typography variant="body2" sx={{ mt: 0.25, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                            {message.text}
                          </Typography>
                        </Box>
                      ))}
                    </Stack>
                  </>
                )}
              </Paper>

              <Paper sx={{ p: 2, border: '1px solid rgba(255,255,255,0.08)', bgcolor: 'rgba(255,255,255,0.03)' }}>
                <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 1 }}>Suggested Questions</Typography>
                <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
                  {suggestions.map((item) => (
                    <Chip
                      key={item.label}
                      label={item.label}
                      size="small"
                      variant="outlined"
                      onClick={() => {
                        setDraft(item.prompt);
                        inputRef.current?.focus();
                      }}
                    />
                  ))}
                </Stack>
              </Paper>

              {messages.map((message) => (
                <Box key={message.id} sx={{ display: 'flex', justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start' }}>
                  <Paper
                    sx={{
                      p: 1.5,
                      maxWidth: '92%',
                      bgcolor: message.role === 'user' ? 'rgba(66,133,244,0.16)' : 'rgba(255,255,255,0.05)',
                      border: '1px solid rgba(255,255,255,0.06)',
                      borderRadius: 2
                    }}
                  >
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.5 }}>
                      {message.role === 'user' ? 'You' : 'Copilot'} · {formatTime(message.timestamp)}
                    </Typography>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.55 }}>
                      {message.text}
                    </Typography>
                    {message.actions?.length ? (
                      <Stack direction="row" spacing={0.5} useFlexGap flexWrap="wrap" sx={{ mt: 1 }}>
                        {message.actions.map((action, index) => (
                          <Chip
                            key={`${message.id}-${index}`}
                            size="small"
                            icon={<OpenInNew />}
                            label={action.type === 'navigate' ? `Open ${action.page}` : action.type === 'download-pack' ? 'Download pack' : 'Action'}
                            variant="outlined"
                          />
                        ))}
                      </Stack>
                    ) : null}
                  </Paper>
                </Box>
              ))}
              <div ref={messagesEndRef} />
            </Stack>
          </Box>

          <Box sx={{ p: 2, borderTop: '1px solid rgba(255,255,255,0.08)' }}>
            <Stack spacing={1.25}>
              <TextField
                inputRef={inputRef}
                fullWidth
                size="small"
                placeholder={`Ask me about ${getRoleLabel(role).toLowerCase()}, reports, navigation, or permitted workflows...`}
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    submitPrompt();
                  }
                }}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={startVoiceCapture} disabled={!voiceActive} color={listening ? 'primary' : 'default'}>
                        {listening ? <MicOff /> : <Mic />}
                      </IconButton>
                    </InputAdornment>
                  )
                }}
              />
              <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <Typography variant="caption" color="text.secondary">
                  {voiceActive
                    ? 'Voice enabled. Speak or type a query.'
                    : 'Text mode only. Enable voice to use speech input and spoken responses.'}
                </Typography>
                <Button variant="contained" startIcon={<Send />} onClick={() => submitPrompt()} disabled={loading || draft.trim().length === 0}>
                  Send
                </Button>
              </Stack>
            </Stack>
          </Box>
        </Box>
      </Drawer>
    </>
  );
};

export default AiBankingCopilotPanel;
