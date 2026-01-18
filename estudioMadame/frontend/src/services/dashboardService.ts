import { apiFetch } from '@/lib/api';
import type { ApiResponse } from '@/types';

export interface DashboardStats {
  active_galleries: number;
  total_clients: number;
  storage_used_bytes: number;
  storage_total_bytes: number;
  storage_percentage: number;
}

export interface DashboardGallery {
  id: string;
  title: string;
  date: string;
  image: string | null;
  status: 'Delivered' | 'Editing' | 'Uploading' | 'Selection';
  photos: number;
  size: string;
}

export const dashboardService = {
  getStats: async () => {
    return apiFetch<ApiResponse<DashboardStats>>('/api/v1/dashboard/stats');
  },

  getRecentGalleries: async (params?: { limit?: number; status_filter?: string }) => {
    const query = new URLSearchParams();
    if (params?.limit) query.append('limit', params.limit.toString());
    if (params?.status_filter) query.append('status_filter', params.status_filter);

    const queryString = query.toString();
    return apiFetch<ApiResponse<DashboardGallery[]>>(`/api/v1/dashboard/recent-galleries${queryString ? '?' + queryString : ''}`);
  },
};
