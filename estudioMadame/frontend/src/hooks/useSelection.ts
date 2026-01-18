import { useState, useCallback } from 'react';

interface SelectableItem {
  id: string | number;
  selected?: boolean;
}

/**
 * Custom hook for managing selection state of items
 * @param initialItems - Array of items with id and optional selected property
 * @returns Object with items, selection state, and selection handlers
 */
export const useSelection = <T extends SelectableItem>(initialItems: T[]) => {
  const [items, setItems] = useState<T[]>(initialItems);
  const [selectAll, setSelectAll] = useState(false);

  const selectedCount = items.filter((item) => item.selected).length;

  const handleSelectAll = useCallback((checked: boolean) => {
    setSelectAll(checked);
    setItems((prevItems) =>
      prevItems.map((item) => ({ ...item, selected: checked }))
    );
  }, []);

  const handleSelectItem = useCallback((id: string | number, checked: boolean) => {
    setItems((prevItems) =>
      prevItems.map((item) =>
        item.id === id ? { ...item, selected: checked } : item
      )
    );
  }, []);

  const handleToggleItem = useCallback((id: string | number) => {
    setItems((prevItems) =>
      prevItems.map((item) =>
        item.id === id ? { ...item, selected: !item.selected } : item
      )
    );
  }, []);

  const clearSelection = useCallback(() => {
    setSelectAll(false);
    setItems((prevItems) =>
      prevItems.map((item) => ({ ...item, selected: false }))
    );
  }, []);

  return {
    items,
    setItems,
    selectAll,
    selectedCount,
    handleSelectAll,
    handleSelectItem,
    handleToggleItem,
    clearSelection,
  };
};
