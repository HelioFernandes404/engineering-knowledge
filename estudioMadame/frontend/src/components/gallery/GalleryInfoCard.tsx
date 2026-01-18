import { Calendar, MapPin, Copy, Image as ImageIcon } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import type { Gallery } from '@/types';

interface GalleryInfoCardProps {
  gallery: Gallery;
}

export const GalleryInfoCard = ({ gallery }: GalleryInfoCardProps) => {
  const publicLink = `${window.location.origin}/gallery/${gallery.id}/login`;

  const handleCopyLink = () => {
    navigator.clipboard.writeText(publicLink);
    toast.success('Public link copied to clipboard');
  };

  return (
    <Card className="overflow-hidden">
      <div className="flex flex-col">
        {/* Cover Image */}
        <div className="relative w-full h-40 bg-muted">
          {gallery.cover_image ? (
            <img
              src={gallery.cover_image}
              alt={gallery.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center text-muted-foreground gap-2">
              <ImageIcon className="h-8 w-8 opacity-20" />
              <span className="text-xs font-medium opacity-50">No cover image</span>
            </div>
          )}
          <div className="absolute top-2 right-2">
            <Badge className="bg-background/80 backdrop-blur-sm text-foreground hover:bg-background/90 border-none">
              {gallery.photo_count} Photos
            </Badge>
          </div>
        </div>

        {/* Details */}
        <div className="p-5 space-y-5">
          <div className="space-y-3">
             <h3 className="font-semibold text-sm uppercase tracking-wider text-muted-foreground">Gallery Info</h3>
             <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2 text-sm text-foreground/80">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  {gallery.event_date || 'No date set'}
                </div>
                <div className="flex items-center gap-2 text-sm text-foreground/80">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  {gallery.location || 'No location set'}
                </div>
             </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase text-muted-foreground tracking-wider">
              Public Link
            </label>
            <div className="flex gap-2">
              <Input
                readOnly
                value={publicLink}
                className="font-mono text-xs bg-muted/50 h-9"
              />
              <Button variant="outline" size="icon" className="h-9 w-9 shrink-0" onClick={handleCopyLink}>
                <Copy className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
