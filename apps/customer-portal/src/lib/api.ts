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
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;

  // Local development port mapping (bypasses missing local API gateway)
  if (import.meta.env.DEV && normalizedBaseUrl === 'http://localhost:9000') {
    if (normalizedPath.startsWith('/ese')) return `http://localhost:9090${normalizedPath}`;
    if (normalizedPath.startsWith('/exec')) return `http://localhost:9009${normalizedPath}`;
    if (normalizedPath.startsWith('/rm')) return `http://localhost:9010${normalizedPath}`;
    if (normalizedPath.startsWith('/customers')) return `http://localhost:9001${normalizedPath}`;
    if (normalizedPath.startsWith('/consents')) return `http://localhost:9002${normalizedPath}`;
    if (normalizedPath.startsWith('/gst')) return `http://localhost:9003${normalizedPath}`;
    if (normalizedPath.startsWith('/aa')) return `http://localhost:9004${normalizedPath}`;
    if (normalizedPath.startsWith('/fhc')) return `http://localhost:9005${normalizedPath}`;
    if (normalizedPath.startsWith('/credit')) return `http://localhost:9006${normalizedPath}`;
    if (normalizedPath.startsWith('/cam')) return `http://localhost:9007${normalizedPath}`;
    if (normalizedPath.startsWith('/ocen')) return `http://localhost:9008${normalizedPath}`;
    if (normalizedPath.startsWith('/ckyc')) return `http://localhost:9011${normalizedPath}`;
    if (normalizedPath.startsWith('/mca')) return `http://localhost:9012${normalizedPath}`;
    if (normalizedPath.startsWith('/epfo')) return `http://localhost:9013${normalizedPath}`;
  }

  if (path === '' || path === '/') {
    return normalizedBaseUrl;
  }

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