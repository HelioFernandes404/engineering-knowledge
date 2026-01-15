import { Upload, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';

interface FileUploadProps {
  label?: string;
  accept?: string;
  maxSize?: string;
  preview?: string | null;
  onFileSelect: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onRemove?: () => void;
  id?: string;
}

export const FileUpload = ({
  label = 'Cover Image',
  accept = 'image/*',
  maxSize = '10MB',
  preview,
  onFileSelect,
  onRemove,
  id = 'file-upload',
}: FileUploadProps) => {
  return (
    <div className="space-y-2">
      {label && <Label>{label}</Label>}
      <div className="relative">
        {preview ? (
          <div className="relative rounded-xl overflow-hidden border-2 border-border">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-48 object-cover"
            />
            {onRemove && (
              <Button
                type="button"
                variant="secondary"
                size="icon"
                className="absolute top-2 right-2 rounded-full"
                onClick={onRemove}
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
        ) : (
          <label
            htmlFor={id}
            className="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-xl cursor-pointer hover:bg-muted/50 transition-colors"
          >
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <Upload className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="mb-2 text-sm text-muted-foreground">
                <span className="font-medium text-primary">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-muted-foreground">
                PNG, JPG, GIF up to {maxSize}
              </p>
            </div>
            <input
              id={id}
              type="file"
              className="hidden"
              accept={accept}
              onChange={onFileSelect}
            />
          </label>
        )}
      </div>
    </div>
  );
};
