import type { GalleryStatus, SyncStatus, PrivacyLevel, GalleryLayout, SortOrder } from './common';

export interface GallerySettings {
  privacy: PrivacyLevel;
  password?: string;
  allow_downloads: boolean;
  mature_content: boolean;
  max_client_selection?: number;
  layout: GalleryLayout;
  default_sort: SortOrder;
}

export interface GalleryStats {
  views: number;
  downloads: number;
  selections: number;
}

export interface Gallery {
  id: string;
  client_id: string;
  client_name: string;
  title: string;
  description?: string;
  status: GalleryStatus;
  cover_image?: string;
  photo_count: number;
  date_created: string;
  event_date?: string;
  location?: string;
  access_token?: string;
  google_drive_folder_id?: string;
  google_drive_folder_name?: string;
  auto_sync_enabled: boolean;
  last_sync_at?: string;
  sync_status: SyncStatus;
  settings?: GallerySettings;
  stats?: GalleryStats;
}

export interface GalleryCreate {
  title: string;
  description?: string;
  client_id: string;
  event_date?: string;
  location?: string;
  cover_image?: string;
  google_drive_folder_id?: string;
  auto_sync_enabled: boolean;
  settings?: Partial<GallerySettings>;
}

export interface GalleryUpdate extends Partial<GalleryCreate> {
  status?: GalleryStatus;
}
