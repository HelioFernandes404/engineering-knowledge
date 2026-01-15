import type {
  GalleryStatus,
  ApprovalStatus,
  DashboardGalleryStatus,
  BadgeVariant
} from '@/types';

/**
 * Gallery Status Utilities
 */
export const getGalleryStatusColor = (status: GalleryStatus): string => {
  const statusColorMap: Record<GalleryStatus, string> = {
    'published': 'bg-green-100 text-green-800 border-green-200',
    'draft': 'bg-yellow-100 text-yellow-800 border-yellow-200',
    'client_selection': 'bg-blue-100 text-blue-800 border-blue-200',
    'archived': 'bg-gray-100 text-gray-800 border-gray-200',
  };

  return statusColorMap[status] || 'bg-gray-100 text-gray-800 border-gray-200';
};

export const getGalleryStatusDotColor = (status: GalleryStatus): string => {
  const statusDotMap: Record<GalleryStatus, string> = {
    'published': 'bg-green-500',
    'draft': 'bg-yellow-500',
    'client_selection': 'bg-blue-500',
    'archived': 'bg-gray-400',
  };

  return statusDotMap[status] || 'bg-gray-400';
};

/**
 * Approval Status Utilities
 */
export const getApprovalStatusColor = (status: ApprovalStatus): string => {
  const statusColorMap: Record<ApprovalStatus, string> = {
    'complete': 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    'changes': 'bg-primary/20 text-primary border-primary/30',
    'awaiting': 'bg-muted/20 text-muted-foreground border-muted/30',
  };

  return statusColorMap[status] || 'bg-muted/20 text-muted-foreground border-muted/30';
};

export const getApprovalStatusDotColor = (status: ApprovalStatus): string => {
  const statusDotMap: Record<ApprovalStatus, string> = {
    'complete': 'bg-emerald-400',
    'changes': 'bg-primary',
    'awaiting': 'bg-muted-foreground',
  };

  return statusDotMap[status] || 'bg-muted-foreground';
};

export const getApprovalStatusLabel = (status: ApprovalStatus): string => {
  const statusLabelMap: Record<ApprovalStatus, string> = {
    'complete': 'Complete',
    'changes': 'Changes Requested',
    'awaiting': 'Awaiting',
  };

  return statusLabelMap[status] || status;
};

export const getApprovalStatusAnimation = (status: ApprovalStatus): string => {
  return status === 'awaiting' ? 'animate-pulse' : '';
};

/**
 * Dashboard Gallery Status Utilities
 */
export const getDashboardStatusVariant = (status: DashboardGalleryStatus): BadgeVariant => {
  const statusVariantMap: Record<DashboardGalleryStatus, BadgeVariant> = {
    'Delivered': 'default',
    'Editing': 'secondary',
    'Uploading': 'outline',
    'Selection': 'outline',
  };

  return statusVariantMap[status] || 'outline';
};

export const getDashboardStatusIconName = (status: DashboardGalleryStatus): string => {
  const statusIconMap: Record<DashboardGalleryStatus, string> = {
    'Delivered': 'CheckCircle2',
    'Editing': 'Clock',
    'Uploading': 'UploadCloud',
    'Selection': 'Image',
  };

  return statusIconMap[status] || '';
};
