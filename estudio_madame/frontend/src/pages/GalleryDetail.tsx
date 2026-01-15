import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Camera,
  Download,
  Eye,
  RefreshCw,
  Image as ImageIcon,
  Plus,
} from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { galleryService } from '@/services/galleryService';
import { photoService, type Photo } from '@/services/photoService';
import { clientService } from '@/services/clientService';
import { GalleryHeader } from '@/components/gallery/GalleryHeader';
import { GalleryInfoCard } from '@/components/gallery/GalleryInfoCard';
import { GalleryStats as StatsCard } from '@/components/gallery/GalleryStats';
import { ClientSidebar } from '@/components/gallery/ClientSidebar';
import { PhotoGridView } from '@/components/gallery/PhotoGridView';
import { PhotoListView } from '@/components/gallery/PhotoListView';
import { ViewModeToggle } from '@/components/ViewModeToggle';
import { useViewMode } from '@/hooks/useViewMode';
import type { Gallery, Client } from '@/types';

const GalleryDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [gallery, setGallery] = useState<Gallery | null>(null);
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [client, setClient] = useState<Client | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const { viewMode, setViewMode } = useViewMode('grid');

  const fetchData = async () => {
    if (!id) return;
    setIsLoading(true);
    try {
      const galleryRes = await galleryService.get(id);
      setGallery(galleryRes.data);

      const [photosRes, clientRes] = await Promise.all([
        photoService.list(id, { limit: 100 }),
        clientService.get(galleryRes.data.client_id)
      ]);
      
      setPhotos(photosRes.data);
      setClient(clientRes.data);
    } catch (error) {
      toast.error('Failed to load gallery data');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleSync = async () => {
    if (!id) return;
    setIsSyncing(true);
    try {
      await photoService.sync(id);
      toast.success('Sync started!');
      fetchData();
    } catch (error) {
      toast.error('Sync failed');
    } finally {
      setIsSyncing(false);
    }
  };

  const handleDeletePhoto = async (photoId: string) => {
    if (window.confirm('Are you sure you want to delete this photo? This action cannot be undone.')) {
      try {
        await photoService.delete(photoId);
        setPhotos(photos.filter(p => p.id !== photoId));
        toast.success('Photo deleted successfully');
      } catch (error) {
        toast.error('Failed to delete photo');
      }
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <div className="border-b bg-muted/30 h-16 flex items-center px-6">
           <Skeleton className="h-8 w-64" />
        </div>
        <main className="container max-w-7xl mx-auto px-6 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div className="lg:col-span-3 space-y-8">
               <div className="flex justify-between items-center">
                  <Skeleton className="h-10 w-48" />
                  <Skeleton className="h-10 w-32" />
               </div>
               <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
                    <Skeleton key={i} className="aspect-[4/5] rounded-lg" />
                  ))}
               </div>
            </div>
            <div className="space-y-8">
              <Skeleton className="h-64 w-full" />
              <Skeleton className="h-48 w-full" />
            </div>
          </div>
        </main>
      </div>
    );
  }

  if (!gallery) {
    return (
      <div className="p-20 text-center space-y-4">
        <ImageIcon className="h-12 w-12 mx-auto text-muted-foreground opacity-20" />
        <h2 className="text-xl font-semibold">Gallery not found</h2>
        <Button onClick={() => navigate('/galleries')}>Go Back to Galleries</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <GalleryHeader
        title={gallery.title}
        status={gallery.status} 
        backLink="/galleries"
        onShare={() => {
           navigator.clipboard.writeText(`${window.location.origin}/gallery/${gallery.id}/login`);
           toast.success('Public link copied to clipboard!');
        }}
        onPreview={() => {
          window.open(`/gallery/${gallery.id}/view`, '_blank');
        }}
      />

      <main className="container max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-3 space-y-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                 <h2 className="text-2xl font-bold tracking-tight">Gallery Content</h2>
                 <div className="flex items-center gap-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={handleSync}
                        disabled={isSyncing}
                        className="gap-2 h-9"
                    >
                        <RefreshCw className={`h-4 w-4 ${isSyncing ? 'animate-spin' : ''}`} />
                        Sync Drive
                    </Button>
                    <Button
                        variant="default"
                        size="sm"
                        className="gap-2 h-9"
                        onClick={() => toast.info('Manual upload coming soon')}
                    >
                        <Plus className="h-4 w-4" />
                        Add Photos
                    </Button>
                 </div>
              </div>
              <ViewModeToggle viewMode={viewMode} onViewModeChange={setViewMode} />
            </div>

            {photos.length > 0 ? (
              viewMode === 'grid' ? (
                <PhotoGridView 
                  photos={photos} 
                  onDelete={handleDeletePhoto}
                />
              ) : (
                <PhotoListView 
                  photos={photos} 
                  onDelete={handleDeletePhoto}
                />
              )
            ) : (
              <div className="flex flex-col items-center justify-center py-20 bg-muted/20 rounded-xl border-2 border-dashed space-y-4">
                <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
                   <ImageIcon className="h-8 w-8 text-muted-foreground opacity-40" />
                </div>
                <div className="text-center">
                  <h3 className="font-semibold text-lg">No photos yet</h3>
                  <p className="text-sm text-muted-foreground max-w-xs mx-auto">
                    This gallery is empty. Sync with Google Drive or upload photos manually to get started.
                  </p>
                </div>
                <Button variant="outline" onClick={handleSync} disabled={isSyncing}>
                  <RefreshCw className={`h-4 w-4 mr-2 ${isSyncing ? 'animate-spin' : ''}`} />
                  Sync Google Drive
                </Button>
              </div>
            )}
          </div>

          <div className="space-y-8">
            <GalleryInfoCard gallery={gallery} />
            <StatsCard 
              stats={[
                { label: 'Photos', value: photos.length, icon: Camera },
                { label: 'Views', value: gallery.stats?.views || 0, icon: Eye },
                { label: 'Downloads', value: gallery.stats?.downloads || 0, icon: Download },
              ]} 
            />
            <ClientSidebar client={client} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default GalleryDetail;
