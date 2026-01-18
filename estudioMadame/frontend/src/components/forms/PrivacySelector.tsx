import { Globe, Lock, KeyRound } from 'lucide-react';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import type { LucideIcon } from 'lucide-react';

interface PrivacyOption {
  value: string;
  icon: LucideIcon;
  label: string;
  description: string;
}

interface PrivacySelectorProps {
  value: string;
  onValueChange: (value: string) => void;
  label?: string;
}

const DEFAULT_OPTIONS: PrivacyOption[] = [
  {
    value: 'public',
    icon: Globe,
    label: 'Public',
    description: 'Visible to everyone.',
  },
  {
    value: 'private',
    icon: Lock,
    label: 'Private',
    description: 'Only you can view.',
  },
  {
    value: 'password',
    icon: KeyRound,
    label: 'Protected',
    description: 'Requires a password.',
  },
];

export const PrivacySelector = ({
  value,
  onValueChange,
  label = 'Privacy',
}: PrivacySelectorProps) => {
  return (
    <div className="space-y-3">
      <Label>{label}</Label>
      <RadioGroup value={value} onValueChange={onValueChange}>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {DEFAULT_OPTIONS.map((option) => (
            <label
              key={option.value}
              className={`relative flex flex-col p-4 border rounded-xl cursor-pointer hover:bg-muted/50 transition-all ${
                value === option.value
                  ? 'border-primary bg-primary/5 ring-1 ring-primary'
                  : 'border-border'
              }`}
            >
              <RadioGroupItem
                value={option.value}
                id={option.value}
                className="sr-only"
              />
              <div className="flex items-center gap-2 mb-1">
                <option.icon
                  className={`h-5 w-5 ${
                    value === option.value ? 'text-primary' : 'text-muted-foreground'
                  }`}
                />
                <span className="font-medium text-sm">{option.label}</span>
              </div>
              <span className="text-xs text-muted-foreground">
                {option.description}
              </span>
            </label>
          ))}
        </div>
      </RadioGroup>
    </div>
  );
};
