import { apiFetch } from '@/lib/api';
import type { Gallery, GalleryCreate, GalleryUpdate, GalleryStatus, ApiResponse } from '@/types';

export const galleryService = {
  list: async (params: {
    page?: number;
    limit?: number;
    status?: GalleryStatus;
    client_id?: string;
    search?: string;
    sort_by?: string;
    order?: 'asc' | 'desc';
  } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) query.append(key, value.toString());
    });
    
    const queryString = query.toString();
    const endpoint = `/api/v1/galleries${queryString ? '?' + queryString : ''}`;
    
    return apiFetch<ApiResponse<Gallery[]>>(endpoint);
  },

  get: async (id: string) => {
    return apiFetch<ApiResponse<Gallery>>(`/api/v1/galleries/${id}`);
  },

  create: async (data: GalleryCreate) => {
    return apiFetch<ApiResponse<Gallery>>('/api/v1/galleries', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  update: async (id: string, data: GalleryUpdate) => {
    return apiFetch<ApiResponse<Gallery>>(`/api/v1/galleries/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  delete: async (id: string) => {
    return apiFetch<void>(`/api/v1/galleries/${id}`, {
      method: 'DELETE',
    });
  },
};
