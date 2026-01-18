import { apiFetch } from '@/lib/api';
import type { ApiResponse } from '@/types';
import type { Client, ClientCreate, ClientUpdate } from '@/types/client';

export const clientService = {
  list: async (params?: { page?: number; limit?: number; search?: string }) => {
    const query = new URLSearchParams();
    if (params?.page) query.append('page', params.page.toString());
    if (params?.limit) query.append('limit', params.limit.toString());
    if (params?.search) query.append('search', params.search);

    const queryString = query.toString();
    return apiFetch<ApiResponse<Client[]>>(`/api/v1/clients${queryString ? '?' + queryString : ''}`);
  },

  get: async (id: string) => {
    return apiFetch<ApiResponse<Client>>(`/api/v1/clients/${id}`);
  },

  create: async (data: ClientCreate) => {
    return apiFetch<ApiResponse<Client>>('/api/v1/clients', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  update: async (id: string, data: ClientUpdate) => {
    return apiFetch<ApiResponse<Client>>(`/api/v1/clients/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  delete: async (id: string) => {
    return apiFetch<void>(`/api/v1/clients/${id}`, {
      method: 'DELETE',
    });
  },

  getGalleries: async (id: string) => {
    return apiFetch<ApiResponse<any[]>>(`/api/v1/clients/${id}/galleries`);
  },
};
