import { useState, useCallback, useMemo } from 'react';

type SortDirection = 'asc' | 'desc';

interface UseFiltersOptions<T> {
  items: T[];
  initialFilters?: Record<string, any>;
  initialSort?: {
    key: keyof T;
    direction: SortDirection;
  };
}

/**
 * Custom hook for managing filters and sorting
 * @param items - Array of items to filter and sort
 * @param initialFilters - Initial filter values
 * @param initialSort - Initial sort configuration
 * @returns Object with filtered items, filters state, and handlers
 */
export const useFilters = <T extends Record<string, any>>({
  items,
  initialFilters = {},
  initialSort,
}: UseFiltersOptions<T>) => {
  const [filters, setFilters] = useState<Record<string, any>>(initialFilters);
  const [sortKey, setSortKey] = useState<keyof T | undefined>(initialSort?.key);
  const [sortDirection, setSortDirection] = useState<SortDirection>(
    initialSort?.direction || 'asc'
  );

  const setFilter = useCallback((key: string, value: any) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  }, []);

  const removeFilter = useCallback((key: string) => {
    setFilters((prev) => {
      const newFilters = { ...prev };
      delete newFilters[key];
      return newFilters;
    });
  }, []);

  const clearFilters = useCallback(() => {
    setFilters({});
  }, []);

  const setSort = useCallback((key: keyof T, direction?: SortDirection) => {
    setSortKey(key);
    setSortDirection(direction || 'asc');
  }, []);

  const toggleSortDirection = useCallback(() => {
    setSortDirection((prev) => (prev === 'asc' ? 'desc' : 'asc'));
  }, []);

  const clearSort = useCallback(() => {
    setSortKey(undefined);
    setSortDirection('asc');
  }, []);

  const filteredAndSortedItems = useMemo(() => {
    let result = [...items];

    // Apply filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        result = result.filter((item) => {
          const itemValue = item[key];

          if (typeof value === 'string') {
            return String(itemValue).toLowerCase().includes(value.toLowerCase());
          }

          return itemValue === value;
        });
      }
    });

    // Apply sorting
    if (sortKey) {
      result.sort((a, b) => {
        const aValue = a[sortKey];
        const bValue = b[sortKey];

        if (aValue === bValue) return 0;

        const comparison = aValue < bValue ? -1 : 1;
        return sortDirection === 'asc' ? comparison : -comparison;
      });
    }

    return result;
  }, [items, filters, sortKey, sortDirection]);

  const activeFiltersCount = useMemo(() => {
    return Object.values(filters).filter(
      (value) => value !== undefined && value !== null && value !== ''
    ).length;
  }, [filters]);

  return {
    filters,
    sortKey,
    sortDirection,
    filteredItems: filteredAndSortedItems,
    setFilter,
    removeFilter,
    clearFilters,
    setSort,
    toggleSortDirection,
    clearSort,
    activeFiltersCount,
    hasActiveFilters: activeFiltersCount > 0,
    hasSorting: sortKey !== undefined,
  };
};
