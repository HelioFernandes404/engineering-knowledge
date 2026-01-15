import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Plus,
  ChevronDown,
  Eye,
  MoreHorizontal,
  Share2,
  Trash2,
} from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

import { GalleryStatusBadge } from '@/components/StatusBadge';
import { ViewModeToggle } from '@/components/ViewModeToggle';
import { Pagination } from '@/components/Pagination';
import { SearchFilterBar } from '@/components/SearchFilterBar';
import { BulkActionsBar } from '@/components/BulkActionsBar';
import { useSelection } from '@/hooks/useSelection';
import { useViewMode } from '@/hooks/useViewMode';
import { galleryService } from '@/services/galleryService';
import type { Gallery, GalleryStatus } from '@/types';

const GalleryPage = () => {
  const [galleries, setGalleries] = useState<Gallery[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<GalleryStatus | undefined>();
  const [page, setPage] = useState(1);

  const { viewMode, setViewMode } = useViewMode('list');
  const {
    selectedCount,
    handleSelectAll,
    handleSelectItem,
    selectAll,
  } = useSelection<Gallery>(galleries);

  const fetchGalleries = async () => {
    setIsLoading(true);
    try {
      const response = await galleryService.list({
        search,
        status: statusFilter,
        page,
      });
      setGalleries(response.data);
    } catch (error: any) {
      toast.error('Failed to fetch galleries');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchGalleries();
  }, [search, statusFilter, page]);

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this gallery?')) {
      try {
        await galleryService.delete(id);
        toast.success('Gallery deleted');
        fetchGalleries();
      } catch (error) {
        toast.error('Failed to delete gallery');
      }
    }
  };

  return (
    <div className="container max-w-7xl mx-auto px-6 pt-10">
      <header className="mb-10 flex items-start justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Galleries</h1>
          <p className="text-base text-muted-foreground mt-1">
            Manage and view all your client photo galleries.
          </p>
        </div>
        <Link to="/gallery/create">
          <Button className="gap-2 shadow-lg">
            <Plus className="h-5 w-5" />
            <span className="font-medium tracking-wide">Create New Gallery</span>
          </Button>
        </Link>
      </header>

      <SearchFilterBar
        searchPlaceholder="Search galleries by name or client..."
        onSearchChange={setSearch}
        filters={
          <>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="gap-2">
                  <span>{statusFilter || 'All Status'}</span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setStatusFilter(undefined)}>All Status</DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter('published')}>Published</DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter('draft')}>Draft</DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter('client_selection')}>Client Selection</DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter('archived')}>Archived</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </>
        }
        actions={<ViewModeToggle viewMode={viewMode} onViewModeChange={setViewMode} />}
      />

      <BulkActionsBar
        selectedCount={selectedCount}
        selectAll={selectAll}
        onSelectAllChange={(checked) => handleSelectAll(checked as boolean)}
      />

      <div className="mt-6">
        {isLoading ? (
          <div className="text-center py-10">Loading galleries...</div>
        ) : galleries.length === 0 ? (
          <div className="text-center py-10 text-muted-foreground">No galleries found.</div>
        ) : (
          <div className="rounded-md border bg-card">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-12"></TableHead>
                  <TableHead>Gallery</TableHead>
                  <TableHead>Client</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Photos</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {galleries.map((gallery) => (
                  <TableRow key={gallery.id}>
                    <TableCell>
                      <input
                        type="checkbox"
                        className="h-4 w-4"
                        onChange={(e) => handleSelectItem(gallery.id, e.target.checked)}
                      />
                    </TableCell>
                    <TableCell className="font-medium">
                      <Link to={`/gallery/${gallery.id}`} className="hover:underline">
                        {gallery.title}
                      </Link>
                    </TableCell>
                    <TableCell>{gallery.client_name}</TableCell>
                    <TableCell>
                      <GalleryStatusBadge status={gallery.status} />
                    </TableCell>
                    <TableCell>{gallery.photo_count}</TableCell>
                    <TableCell>
                      {new Date(gallery.date_created).toLocaleDateString()}
                    </TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem asChild>
                            <Link to={`/gallery/${gallery.id}`} className="flex items-center gap-2">
                              <Eye className="h-4 w-4" /> View Details
                            </Link>
                          </DropdownMenuItem>
                          <DropdownMenuItem className="flex items-center gap-2">
                            <Share2 className="h-4 w-4" /> Share
                          </DropdownMenuItem>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem
                            className="flex items-center gap-2 text-destructive"
                            onClick={() => handleDelete(gallery.id)}
                          >
                            <Trash2 className="h-4 w-4" /> Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>

      <div className="mt-8 flex justify-center">
        <Pagination
          currentPage={page}
          totalPages={1}
          onPageChange={setPage}
        />
      </div>
    </div>
  );
};

export default GalleryPage;
