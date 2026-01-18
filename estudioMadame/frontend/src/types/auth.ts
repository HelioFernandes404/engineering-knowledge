export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'photographer' | 'client';
}

export interface LoginResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

export interface ClientLoginResponse {
  client: import('./client').Client;
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

export interface RefreshTokenResponse {
  access_token: string;
  expires_in: number;
}

export interface GalleryAccessTokenResponse {
  gallery_access_token: string;
  gallery_id: string;
  expires_at: string;
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
}
