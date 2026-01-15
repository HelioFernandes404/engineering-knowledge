import { Mail, Phone, ExternalLink, User } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import type { Client } from '@/types';

interface ClientSidebarProps {
  client?: Client | null;
  onViewProfile?: () => void;
}

export const ClientSidebar = ({ client, onViewProfile }: ClientSidebarProps) => {
  if (!client) {
    return (
      <Card>
        <CardHeader className="pb-4">
          <CardTitle className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">Client Details</CardTitle>
        </CardHeader>
        <CardContent className="pt-0 pb-6 flex items-center justify-center">
          <p className="text-xs text-muted-foreground opacity-60 italic">No client data available</p>
        </CardContent>
      </Card>
    );
  }

  const initials = client.name
    .split(' ')
    .filter(Boolean)
    .map((n) => n[0])
    .join('')
    .toUpperCase();

  return (
    <Card className="overflow-hidden">
      <CardHeader className="pb-4 border-b bg-muted/30">
        <CardTitle className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">Client Details</CardTitle>
      </CardHeader>
      <CardContent className="pt-6 space-y-6">
        <div className="flex items-center gap-4">
          <Avatar className="h-12 w-12 border-2 border-background shadow-sm">
            <AvatarImage src={client.avatar} />
            <AvatarFallback className="bg-primary/10 text-primary font-bold">
               {initials || <User className="h-5 w-5" />}
            </AvatarFallback>
          </Avatar>
          <div className="space-y-0.5">
            <div className="font-bold text-base leading-tight">{client.name}</div>
            <div className="text-[11px] font-semibold text-primary uppercase tracking-tight">Gallery Owner</div>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center gap-3 text-sm p-2.5 bg-muted/50 rounded-lg border border-transparent hover:border-muted-foreground/10 transition-colors">
            <div className="h-8 w-8 rounded-full bg-background flex items-center justify-center shrink-0">
               <Mail className="h-4 w-4 text-muted-foreground" />
            </div>
            <span className="truncate font-medium">{client.email}</span>
          </div>
          
          {client.phone && (
            <div className="flex items-center gap-3 text-sm p-2.5 bg-muted/50 rounded-lg border border-transparent hover:border-muted-foreground/10 transition-colors">
              <div className="h-8 w-8 rounded-full bg-background flex items-center justify-center shrink-0">
                 <Phone className="h-4 w-4 text-muted-foreground" />
              </div>
              <span className="font-medium">{client.phone}</span>
            </div>
          )}
        </div>

        {onViewProfile && (
          <Button variant="outline" className="w-full gap-2 text-xs font-semibold h-10" onClick={onViewProfile}>
            <ExternalLink className="h-3.5 w-3.5" />
            VIEW FULL PROFILE
          </Button>
        )}
      </CardContent>
    </Card>
  );
};
