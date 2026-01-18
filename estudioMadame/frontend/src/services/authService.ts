import { apiFetch } from '@/lib/api';
import type { 
  LoginResponse, 
  ClientLoginResponse, 
  GalleryAccessTokenResponse,
  ApiResponse 
} from '@/types';

export const authService = {
  login: async (credentials: any) => {
    return apiFetch<ApiResponse<LoginResponse>>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  clientLogin: async (credentials: any) => {
    return apiFetch<ApiResponse<ClientLoginResponse>>('/api/v1/auth/client/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  getGalleryAccess: async (galleryId: string) => {
    return apiFetch<ApiResponse<GalleryAccessTokenResponse>>('/api/v1/auth/gallery-access', {
      method: 'POST',
      body: JSON.stringify({ gallery_id: galleryId }),
    });
  },

  logout: async () => {
    return apiFetch<void>('/api/v1/auth/logout', {
      method: 'POST',
    });
  },
};