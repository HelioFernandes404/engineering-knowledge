import { LayoutGrid, List } from 'lucide-react';
import { Button } from '@/components/ui/button';
import type { ViewMode } from '@/hooks/useViewMode';

interface ViewModeToggleProps {
  viewMode: ViewMode;
  onViewModeChange: (mode: ViewMode) => void;
}

export const ViewModeToggle = ({ viewMode, onViewModeChange }: ViewModeToggleProps) => {
  return (
    <div className="flex items-center rounded-lg border p-1">
      <Button
        variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
        size="icon"
        className="h-8 w-8"
        onClick={() => onViewModeChange('grid')}
        aria-label="Grid view"
      >
        <LayoutGrid className="h-5 w-5" />
      </Button>
      <Button
        variant={viewMode === 'list' ? 'secondary' : 'ghost'}
        size="icon"
        className="h-8 w-8"
        onClick={() => onViewModeChange('list')}
        aria-label="List view"
      >
        <List className="h-5 w-5" />
      </Button>
    </div>
  );
};
