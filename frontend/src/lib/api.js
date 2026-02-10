const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL;
const normalizedBaseUrl =
  rawBaseUrl && rawBaseUrl.trim()
    ? rawBaseUrl.trim().replace(/\/+$/, "")
    : DEFAULT_API_BASE_URL;

export const API_BASE_URL = normalizedBaseUrl;

export function apiUrl(path) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${normalizedBaseUrl}${normalizedPath}`;
}
