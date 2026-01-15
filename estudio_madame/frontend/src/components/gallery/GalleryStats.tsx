import { Card } from '@/components/ui/card';
import type { LucideIcon } from 'lucide-react';

interface Stat {
  label: string;
  value: number;
  icon: LucideIcon;
}

interface GalleryStatsProps {
  stats: Stat[];
  columns?: number;
}

export const GalleryStats = ({ stats, columns = 3 }: GalleryStatsProps) => {
  return (
    <div className={`grid grid-cols-2 sm:grid-cols-${columns} gap-3`}>
      {stats.map((stat, i) => (
        <Card
          key={i}
          className="p-4 flex flex-col items-center justify-center text-center hover:bg-muted/30 transition-colors cursor-default border-muted"
        >
          <div className="p-2 rounded-full bg-primary/5 mb-2">
            <stat.icon className="h-4 w-4 text-primary" />
          </div>
          <span className="text-xl font-bold tracking-tight">{stat.value}</span>
          <span className="text-[10px] text-muted-foreground font-semibold uppercase tracking-wider">
            {stat.label}
          </span>
        </Card>
      ))}
    </div>
  );
};
