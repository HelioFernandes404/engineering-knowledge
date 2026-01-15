import { apiFetch } from '@/lib/api';
import type { ApiResponse } from '@/types';

export interface Approval {
  id: string;
  gallery_id: string;
  gallery_name: string;
  client_id: string;
  client_name: string;
  client_avatar?: string;
  status: 'awaiting' | 'complete' | 'changes';
  selected_count: number;
  total_count: number;
  submitted_at?: string;
  updated_at: string;
}

export const approvalService = {
  list: async (params: { page?: number; limit?: number; status?: string; search?: string } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) query.append(key, value.toString());
    });
    
    const queryString = query.toString();
    const endpoint = `/api/v1/approvals${queryString ? '?' + queryString : ''}`;
    
    return apiFetch<ApiResponse<Approval[]>>(endpoint);
  },

  get: async (id: string) => {
    return apiFetch<ApiResponse<Approval>>(`/api/v1/approvals/${id}`);
  },

  submit: async (approvalId: string, galleryAccessToken: string) => {
    return apiFetch<ApiResponse<{approval_id: string, status: string, submitted_at: string}>>(`/api/v1/approvals/${approvalId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ 
        gallery_access_token: galleryAccessToken
      }),
    });
  },
};