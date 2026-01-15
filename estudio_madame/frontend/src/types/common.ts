export type GalleryStatus = 'published' | 'draft' | 'client_selection' | 'archived';
export type SyncStatus = 'idle' | 'syncing' | 'error';
export type PrivacyLevel = 'public' | 'private' | 'password_protected';
export type GalleryLayout = 'grid' | 'masonry' | 'carousel';
export type SortOrder = 'newest' | 'oldest' | 'name_asc' | 'name_desc';

export type ApprovalStatus = 'awaiting' | 'complete' | 'changes';
export type DashboardGalleryStatus = 'Delivered' | 'Editing' | 'Uploading' | 'Selection';

export type BadgeVariant = 'default' | 'secondary' | 'outline' | 'destructive' | null | undefined;

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export interface ApiResponse<T> {
  data: T;
  meta?: PaginationMeta;
}
