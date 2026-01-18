import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  maxVisiblePages?: number;
}

export const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  maxVisiblePages = 5,
}: PaginationProps) => {
  const getPageNumbers = () => {
    const pages: (number | 'ellipsis')[] = [];

    if (totalPages <= maxVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      pages.push(1);

      let startPage = Math.max(2, currentPage - 1);
      let endPage = Math.min(totalPages - 1, currentPage + 1);

      if (currentPage <= 3) {
        endPage = maxVisiblePages - 1;
      }

      if (currentPage >= totalPages - 2) {
        startPage = totalPages - maxVisiblePages + 2;
      }

      if (startPage > 2) {
        pages.push('ellipsis');
      }

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }

      if (endPage < totalPages - 1) {
        pages.push('ellipsis');
      }

      pages.push(totalPages);
    }

    return pages;
  };

  return (
    <nav aria-label="Pagination" className="mt-8 flex items-center justify-center">
      <ul className="inline-flex items-center space-x-2">
        <li>
          <Button
            variant="outline"
            size="icon"
            className="h-9 w-9"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            <ChevronLeft className="h-4 w-4" />
            <span className="sr-only">Previous</span>
          </Button>
        </li>

        {getPageNumbers().map((page, index) => (
          <li key={`page-${index}`}>
            {page === 'ellipsis' ? (
              <span className="flex h-9 w-9 items-center justify-center text-sm font-medium text-muted-foreground">
                ...
              </span>
            ) : (
              <Button
                variant={page === currentPage ? 'default' : 'outline'}
                size="icon"
                className="h-9 w-9"
                onClick={() => onPageChange(page)}
              >
                {page}
              </Button>
            )}
          </li>
        ))}

        <li>
          <Button
            variant="outline"
            size="icon"
            className="h-9 w-9"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            <ChevronRight className="h-4 w-4" />
            <span className="sr-only">Next</span>
          </Button>
        </li>
      </ul>
    </nav>
  );
};
