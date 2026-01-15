import { useState, useCallback, useMemo } from 'react';

/**
 * Custom hook for managing search state and filtering items
 * @param items - Array of items to search through
 * @param searchKeys - Array of keys to search in each item
 * @returns Object with search query, filtered items, and search handlers
 */
export const useSearch = <T extends Record<string, any>>(
  items: T[],
  searchKeys: (keyof T)[]
) => {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredItems = useMemo(() => {
    if (!searchQuery.trim()) {
      return items;
    }

    const query = searchQuery.toLowerCase();

    return items.filter((item) =>
      searchKeys.some((key) => {
        const value = item[key];
        if (typeof value === 'string') {
          return value.toLowerCase().includes(query);
        }
        if (typeof value === 'number') {
          return value.toString().includes(query);
        }
        return false;
      })
    );
  }, [items, searchQuery, searchKeys]);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const clearSearch = useCallback(() => {
    setSearchQuery('');
  }, []);

  return {
    searchQuery,
    setSearchQuery,
    handleSearch,
    clearSearch,
    filteredItems,
    hasResults: filteredItems.length > 0,
    resultCount: filteredItems.length,
  };
};
