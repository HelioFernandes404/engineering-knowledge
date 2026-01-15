const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('access_token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return {} as T;
  }

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.error || result.detail || 'Something went wrong');
  }

  return result;
}
