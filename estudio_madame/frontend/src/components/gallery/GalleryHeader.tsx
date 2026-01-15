import { Link } from 'react-router-dom';
import { ArrowLeft, Eye, Share2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface GalleryHeaderProps {
  title: string;
  status: string;
  updatedAt?: string;
  onShare?: () => void;
  onPreview?: () => void;
  backLink?: string;
}

export const GalleryHeader = ({
  title,
  status,
  updatedAt = 'Updated 2 hours ago',
  onShare,
  onPreview,
  backLink = '/dashboard',
}: GalleryHeaderProps) => {
  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto max-w-7xl px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to={backLink}>
            <Button variant="ghost" size="icon">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight">{title}</h1>
              <Badge className="uppercase text-[10px]">{status}</Badge>
            </div>
            <span className="text-xs text-muted-foreground font-medium">{updatedAt}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {onPreview && (
            <Button variant="outline" size="sm" className="hidden sm:flex gap-2" onClick={onPreview}>
              <Eye className="h-4 w-4" /> Preview
            </Button>
          )}
          {onShare && (
            <Button size="sm" className="gap-2" onClick={onShare}>
              <Share2 className="h-4 w-4" /> Share
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};
