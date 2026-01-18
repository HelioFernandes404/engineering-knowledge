import { useState, useEffect } from 'react';
import { Heart, Send, Camera, LogOut, X } from 'lucide-react';
import { useParams, useNavigate } from 'react-router-dom';

import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { photoService } from '@/services/photoService';
import { galleryService } from '@/services/galleryService';
import { approvalService } from '@/services/approvalService';
import type { Gallery, Photo } from '@/types';

const ClientGallery = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [gallery, setGallery] = useState<Gallery | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showBanner, setShowBanner] = useState(true);

  const galleryAccessToken = localStorage.getItem(`gallery_access_${id}`) || '';

  useEffect(() => {
    if (!id || !galleryAccessToken) {
      navigate(`/gallery/${id}/login`);
      return;
    }

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const galleryResp = await galleryService.get(id);
        setGallery(galleryResp.data);

        const photosResp = await photoService.listPublic(id, galleryAccessToken, { limit: 100 });
        setPhotos(photosResp.data);
      } catch (err) {
        console.error('Failed to fetch gallery data', err);
        toast.error('Failed to load gallery');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [id, galleryAccessToken, navigate]);

  const togglePhotoSelection = async (photoId: string) => {
    const photo = photos.find(p => p.id === photoId);
    if (!photo) return;

    const newSelected = !photo.selected_by_client;

    if (newSelected && gallery?.settings?.max_client_selection) {
      const currentSelected = photos.filter(p => p.selected_by_client).length;
      if (currentSelected >= gallery.settings.max_client_selection) {
        toast.error('Selection limit reached', {
          description: `You can only select up to ${gallery.settings.max_client_selection} photos.`,
        });
        return;
      }
    }

    try {
      await photoService.select(photoId, newSelected, galleryAccessToken);
      setPhotos(prev => prev.map(item => item.id === photoId ? { ...item, selected_by_client: newSelected } : item));
    } catch (err) {
      toast.error('Failed to update selection');
    }
  };

  const handleSendApproval = async () => {
    const selectedCount = photos.filter(p => p.selected_by_client).length;
    if (selectedCount === 0) {
      toast.error('No photos selected', {
        description: 'Please select at least one photo before sending approval.',
      });
      return;
    }

    try {
      const appsResp = await approvalService.list({ search: gallery?.title });
      const thisApproval = appsResp.data.find(a => a.gallery_id === id);

      if (!thisApproval) {
        toast.error('Approval record not found');
        return;
      }

      await approvalService.submit(thisApproval.id, galleryAccessToken);
      toast.success('Approval sent!', {
        description: `${selectedCount} photos have been sent to your photographer.`,
      });
    } catch (err) {
      toast.error('Failed to send approval');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    localStorage.removeItem(`gallery_access_${id}`);
    navigate(`/gallery/${id}/login`);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="h-8 w-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const selectedCount = photos.filter(p => p.selected_by_client).length;
  const maxSelection = gallery?.settings?.max_client_selection || 0;

  return (
    <div className="min-h-screen bg-background">
      <div className="px-4 sm:px-8 md:px-16 lg:px-24 xl:px-40 flex flex-1 justify-center py-5">
        <div className="flex flex-col w-full max-w-[960px]">

          <header className="sticky top-5 z-10 flex items-center justify-between bg-card/80 backdrop-blur-md p-4 rounded-xl border shadow-sm">
            <div>
              <h1 className="text-lg font-bold">{gallery?.title}</h1>
              <p className="text-xs text-muted-foreground">
                {gallery?.client_name} • {selectedCount} {maxSelection > 0 ? ` of ${maxSelection} ` : ''} photos selected
              </p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Exit
              </Button>
              <Button size="sm" onClick={handleSendApproval}>
                <Send className="h-4 w-4 mr-2" />
                Send Approval
              </Button>
            </div>
          </header>

          {showBanner && maxSelection > 0 && (
            <div className="relative mt-5 bg-primary/10 border border-primary/20 rounded-lg p-4 flex items-center gap-3">
              <Camera className="h-5 w-5 text-primary" />
              <div className="flex-1">
                <p className="text-sm font-medium text-primary">Photo Selection Guide</p>
                <p className="text-xs text-primary/80">
                  You can select up to <strong>{maxSelection}</strong> photos for final processing. Click the heart icon on any photo to add it to your selection.
                </p>
              </div>
              <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setShowBanner(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          )}

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mt-8">
            {photos.map((photo) => (
              <div key={photo.id} className="group relative aspect-square rounded-lg overflow-hidden border bg-muted">
                <img
                  src={photo.url}
                  alt={photo.filename}
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                <button
                  onClick={() => togglePhotoSelection(photo.id)}
                  className={`absolute top-3 right-3 p-2 rounded-full transition-colors ${photo.selected_by_client ? 'bg-primary text-primary-foreground' : 'bg-black/40 text-white hover:bg-black/60'}`}
                >
                  <Heart className={`h-5 w-5 ${photo.selected_by_client ? 'fill-current' : ''}`} />
                </button>
              </div>
            ))}
          </div>

          {photos.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20">
              <Camera className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-muted-foreground">No photos found in this gallery.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClientGallery;
