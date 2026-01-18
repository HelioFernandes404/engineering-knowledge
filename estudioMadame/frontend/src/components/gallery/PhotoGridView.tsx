import { Edit2, Trash2, Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface Photo {
  id: string;
  url: string;
  filename: string;
  size?: number | string;
  selected_by_client?: boolean;
}

interface PhotoGridViewProps {
  photos: Photo[];
  onDelete?: (id: string) => void;
  onEdit?: (id: string) => void;
}

export const PhotoGridView = ({ photos, onDelete, onEdit }: PhotoGridViewProps) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      {photos.map((photo) => (
        <div
          key={photo.id}
          className={`group relative aspect-[4/5] bg-muted rounded-lg overflow-hidden border shadow-sm hover:shadow-md transition-all ${
            photo.selected_by_client ? 'ring-2 ring-primary ring-offset-2' : ''
          }`}
        >
          <img
            src={photo.url}
            alt={photo.filename}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />

          {/* Client Selected Badge */}
          {photo.selected_by_client && (
            <div className="absolute top-2 left-2 z-10">
              <Badge className="gap-1 bg-primary text-primary-foreground border-none">
                <Heart className="h-3 w-3 fill-current" />
                Selected
              </Badge>
            </div>
          )}

          {/* Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

          {/* Top Right Actions */}
          <div className="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-all duration-200 translate-y-[-10px] group-hover:translate-y-0">
            {onEdit && (
              <Button
                size="icon"
                variant="secondary"
                className="h-8 w-8 shadow-sm"
                onClick={() => onEdit(photo.id)}
              >
                <Edit2 className="h-3.5 w-3.5" />
              </Button>
            )}
            {onDelete && (
              <Button
                size="icon"
                variant="secondary"
                className="h-8 w-8 shadow-sm hover:bg-destructive hover:text-destructive-foreground"
                onClick={() => onDelete(photo.id)}
              >
                <Trash2 className="h-3.5 w-3.5" />
              </Button>
            )}
          </div>

          {/* Bottom Info */}
          <div className="absolute bottom-0 left-0 right-0 p-3 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <p className="text-xs font-medium truncate">{photo.filename}</p>
            <p className="text-[10px] text-white/70">{photo.size}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
