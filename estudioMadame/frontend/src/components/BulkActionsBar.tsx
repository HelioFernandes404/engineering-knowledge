import { Checkbox } from '@/components/ui/checkbox';
import type { ReactNode } from 'react';

interface BulkActionsBarProps {
  selectedCount: number;
  selectAll?: boolean;
  onSelectAllChange?: (checked: boolean) => void;
  actions?: ReactNode;
}

export const BulkActionsBar = ({
  selectedCount,
  selectAll,
  onSelectAllChange,
  actions,
}: BulkActionsBarProps) => {
  if (selectedCount === 0) {
    return null;
  }

  return (
    <div className="flex h-14 items-center justify-between rounded-lg border bg-muted/50 px-4 mb-6">
      <div className="flex items-center gap-4">
        {onSelectAllChange && (
          <div className="flex items-center space-x-2">
            <Checkbox
              id="select-all"
              checked={selectAll}
              onCheckedChange={onSelectAllChange}
            />
            <label htmlFor="select-all" className="text-sm font-medium">
              Select All
            </label>
          </div>
        )}
        <div className="flex items-center gap-2">
          <p className="text-sm font-medium">{selectedCount} items selected</p>
          {actions && (
            <>
              <div className="mx-2 h-6 w-px bg-border" />
              {actions}
            </>
          )}
        </div>
      </div>
    </div>
  );
};
