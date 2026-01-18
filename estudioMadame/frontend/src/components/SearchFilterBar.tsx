import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import type { ReactNode } from 'react';

interface SearchFilterBarProps {
  searchPlaceholder?: string;
  searchValue?: string;
  onSearchChange?: (value: string) => void;
  filters?: ReactNode;
  actions?: ReactNode;
}

export const SearchFilterBar = ({
  searchPlaceholder = 'Search...',
  searchValue,
  onSearchChange,
  filters,
  actions,
}: SearchFilterBarProps) => {
  return (
    <div className="mb-6 flex flex-col gap-4">
      <div className="flex items-center justify-between gap-4">
        {/* Search Input */}
        {onSearchChange && (
          <div className="relative flex-grow max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-5 w-5" />
            <Input
              className="pl-10"
              placeholder={searchPlaceholder}
              type="text"
              value={searchValue}
              onChange={(e) => onSearchChange(e.target.value)}
            />
          </div>
        )}

        {/* Filters and Actions */}
        <div className="flex items-center gap-2">
          {filters}
          {actions}
        </div>
      </div>
    </div>
  );
};
