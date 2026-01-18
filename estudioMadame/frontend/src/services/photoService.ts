import { apiFetch } from '@/lib/api';
import type { ApiResponse } from '@/types';

export interface Photo {
  id: string;
  url: string;
  filename: string;
  size?: number;
  width?: number;
  height?: number;
  selected_by_client: boolean;
  date_taken?: string;
  google_drive_web_view_link?: string;
  google_drive_thumbnail_link?: string;
}

export const photoService = {
  list: async (galleryId: string, params: { page?: number; limit?: number; selected?: boolean } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) query.append(key, value.toString());
    });
    
    const queryString = query.toString();
    const endpoint = `/api/v1/galleries/${galleryId}/photos${queryString ? '?' + queryString : ''}`;
    
    return apiFetch<ApiResponse<Photo[]>>(endpoint);
  },

  listPublic: async (galleryId: string, accessToken: string, params: { page?: number; limit?: number } = {}) => {
    const query = new URLSearchParams();
    query.append('access_token', accessToken);
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) query.append(key, value.toString());
    });
    
    const queryString = query.toString();
    const endpoint = `/api/v1/galleries/${galleryId}/photos/public${queryString ? '?' + queryString : ''}`;
    
    return apiFetch<ApiResponse<Photo[]>>(endpoint);
  },

  select: async (photoId: string, selected: boolean, galleryAccessToken: string) => {
    return apiFetch<ApiResponse<{id: string, selected_by_client: boolean}>>(`/api/v1/photos/${photoId}/select`, {
      method: 'POST',
      body: JSON.stringify({ 
        selected,
        gallery_access_token: galleryAccessToken
      }),
    });
  },

  delete: async (photoId: string) => {
    return apiFetch<void>(`/api/v1/photos/${photoId}`, {
      method: 'DELETE',
    });
  },

  sync: async (galleryId: string) => {
    return apiFetch<ApiResponse<any>>(`/api/v1/integration/google-drive/sync/${galleryId}`, {
      method: 'POST',
    });
  },
};