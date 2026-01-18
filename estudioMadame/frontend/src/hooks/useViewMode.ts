import { useState, useCallback } from 'react';

export type ViewMode = 'grid' | 'list';

/**
 * Custom hook for managing view mode (grid/list) state
 * @param initialMode - Initial view mode (default: 'list')
 * @returns Object with view mode state and setter
 */
export const useViewMode = (initialMode: ViewMode = 'list') => {
  const [viewMode, setViewMode] = useState<ViewMode>(initialMode);

  const toggleViewMode = useCallback(() => {
    setViewMode((prev) => (prev === 'grid' ? 'list' : 'grid'));
  }, []);

  const isGridView = viewMode === 'grid';
  const isListView = viewMode === 'list';

  return {
    viewMode,
    setViewMode,
    toggleViewMode,
    isGridView,
    isListView,
  };
};
