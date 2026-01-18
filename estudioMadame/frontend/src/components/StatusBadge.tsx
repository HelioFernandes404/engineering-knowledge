import { Badge } from '@/components/ui/badge';
import {
  getGalleryStatusColor,
  getGalleryStatusDotColor,
  getApprovalStatusColor,
  getApprovalStatusDotColor,
  getApprovalStatusLabel,
  getApprovalStatusAnimation,
  getDashboardStatusVariant,
} from '@/utils/status';
import type { GalleryStatus, ApprovalStatus, DashboardGalleryStatus } from '@/types';

interface GalleryStatusBadgeProps {
  status: GalleryStatus;
}

export const GalleryStatusBadge = ({ status }: GalleryStatusBadgeProps) => {
  return (
    <Badge variant="outline" className={`gap-1.5 ${getGalleryStatusColor(status)}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${getGalleryStatusDotColor(status)}`} />
      {status}
    </Badge>
  );
};

interface ApprovalStatusBadgeProps {
  status: ApprovalStatus;
}

export const ApprovalStatusBadge = ({ status }: ApprovalStatusBadgeProps) => {
  const animation = getApprovalStatusAnimation(status);

  return (
    <Badge className={getApprovalStatusColor(status)}>
      <span className={`mr-1.5 h-2 w-2 rounded-full ${getApprovalStatusDotColor(status)} ${animation}`} />
      {getApprovalStatusLabel(status)}
    </Badge>
  );
};

interface DashboardStatusBadgeProps {
  status: DashboardGalleryStatus;
  icon?: React.ReactNode;
  children?: React.ReactNode;
}

export const DashboardStatusBadge = ({ status, icon, children }: DashboardStatusBadgeProps) => {
  return (
    <Badge variant={getDashboardStatusVariant(status)}>
      {icon}
      {children || status}
    </Badge>
  );
};
