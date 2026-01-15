import { Trash2, Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface Photo {
  id: string;
  url: string;
  filename: string;
  size?: number | string;
  time?: string;
  selected_by_client?: boolean;
}

interface PhotoListViewProps {
  photos: Photo[];
  onDelete?: (id: string) => void;
}

export const PhotoListView = ({ photos, onDelete }: PhotoListViewProps) => {
  return (
    <div className="bg-background rounded-lg border shadow-sm overflow-hidden">
      <table className="w-full text-left text-sm">
        <thead className="bg-muted border-b text-muted-foreground uppercase text-xs font-semibold">
          <tr>
            <th className="px-6 py-4 font-medium">Media</th>
            <th className="px-6 py-4 font-medium">Filename</th>
            <th className="px-6 py-4 font-medium">Size</th>
            <th className="px-6 py-4 font-medium">Status</th>
            <th className="px-6 py-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {photos.map((photo) => (
            <tr key={photo.id} className="group hover:bg-muted/50 transition-colors">
              <td className="px-6 py-3">
                <div className="h-10 w-10 rounded overflow-hidden bg-muted border relative">
                  <img src={photo.url} alt="" className="h-full w-full object-cover" />
                  {photo.selected_by_client && (
                    <div className="absolute inset-0 bg-primary/20 flex items-center justify-center">
                       <Heart className="h-4 w-4 fill-primary text-primary" />
                    </div>
                  )}
                </div>
              </td>
              <td className="px-6 py-3 font-medium">
                <div className="flex flex-col">
                  <span>{photo.filename}</span>
                </div>
              </td>
              <td className="px-6 py-3 text-muted-foreground font-mono text-xs">
                {photo.size}
              </td>
              <td className="px-6 py-3">
                {photo.selected_by_client ? (
                  <Badge variant="outline" className="gap-1 text-primary border-primary/20 bg-primary/5">
                    <Heart className="h-3 w-3 fill-current" />
                    Selected
                  </Badge>
                ) : (
                  <span className="text-muted-foreground text-xs">Awaiting</span>
                )}
              </td>
              <td className="px-6 py-3 text-right">
                <div className="flex items-center justify-end gap-2">
                  {onDelete && (
                    <Button
                      size="icon"
                      variant="ghost"
                      className="h-8 w-8 text-muted-foreground hover:text-destructive"
                      onClick={() => onDelete(photo.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
