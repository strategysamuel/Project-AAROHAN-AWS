function requireEnv(value: string | undefined, name: string): string {
  if (!value) {
    // In deployed environments, env vars may be injected at runtime.
    // Return empty string rather than throwing to prevent white-screen crashes.
    if (import.meta.env.DEV) {
      console.warn(`[AAROHAN] Warning: ${name} is not set. API calls will fail until this is configured.`);
    }
    return '';
  }

  return value;
}

export const apiBaseUrl = requireEnv(import.meta.env.VITE_API_BASE_URL, 'VITE_API_BASE_URL');
export const authApiBaseUrl = requireEnv(
  import.meta.env.VITE_AUTH_API_BASE_URL || import.meta.env.VITE_API_BASE_URL,
  'VITE_AUTH_API_BASE_URL'
);

export function apiUrl(path: string): string {
  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  const normalizedBaseUrl = apiBaseUrl.replace(/\/$/, '');
  if (path === '' || path === '/') {
    return normalizedBaseUrl;
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${normalizedBaseUrl}${normalizedPath}`;
}

export function authUrl(path: string): string {
  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  const normalizedBaseUrl = authApiBaseUrl.replace(/\/$/, '');
  if (path === '' || path === '/') {
    return normalizedBaseUrl;
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${normalizedBaseUrl}${normalizedPath}`;
}