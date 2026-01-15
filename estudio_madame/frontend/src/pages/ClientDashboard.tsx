import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'sonner';
import { 
  Image as ImageIcon, 
  Calendar, 
  ChevronRight, 
  LogOut,
  User
} from 'lucide-react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { apiFetch } from '@/lib/api';
import type { Gallery, ApiResponse } from '@/types';

export default function ClientDashboard() {
  const [galleries, setGalleries] = useState<Gallery[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const client = JSON.parse(localStorage.getItem('client') || '{}');

  useEffect(() => {
    async function fetchGalleries() {
      try {
        const response = await apiFetch<ApiResponse<Gallery[]>>('/api/v1/clients/me/galleries');
        setGalleries(response.data);
      } catch (error: any) {
        toast.error('Erro ao carregar galerias');
      } finally {
        setIsLoading(false);
      }
    }
    fetchGalleries();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('client');
    window.location.href = '/client/login';
  };

  return (
    <div className="min-h-screen bg-muted/30 pb-12">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-bold">
              EM
            </div>
            <span className="font-bold text-xl hidden sm:inline-block">Estúdio Madame</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm font-medium px-3 py-1 bg-muted rounded-full">
              <User className="w-4 h-4" />
              <span>{client.name || 'Cliente'}</span>
            </div>
            <Button variant="ghost" size="icon" onClick={handleLogout} title="Sair">
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Minhas Galerias</h1>
          <p className="text-muted-foreground">Bem-vindo(a) de volta! Aqui estão suas sessões de fotos.</p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <Card key={i} className="overflow-hidden">
                <Skeleton className="aspect-video w-full" />
                <CardHeader>
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
              </Card>
            ))}
          </div>
        ) : galleries.length === 0 ? (
          <Card className="border-dashed border-2 flex flex-col items-center justify-center p-12 text-center">
            <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
              <ImageIcon className="w-8 h-8 text-muted-foreground" />
            </div>
            <CardTitle>Nenhuma galeria encontrada</CardTitle>
            <CardDescription className="max-w-md mt-2">
              Você ainda não possui galerias vinculadas à sua conta. Entre em contato com o fotógrafo se achar que isso é um erro.
            </CardDescription>
          </Card>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {galleries.map((gallery) => (
              <Card key={gallery.id} className="overflow-hidden group hover:shadow-md transition-shadow">
                <div className="aspect-video relative overflow-hidden bg-muted">
                  {gallery.cover_image ? (
                    <img 
                      src={gallery.cover_image} 
                      alt={gallery.title}
                      className="object-cover w-full h-full transition-transform group-hover:scale-105"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-muted-foreground">
                      <ImageIcon className="w-12 h-12 opacity-20" />
                    </div>
                  )}
                  <div className="absolute top-2 right-2">
                    <Badge variant={gallery.status === 'published' ? 'default' : 'secondary'}>
                      {gallery.status === 'published' ? 'Publicada' : 'Rascunho'}
                    </Badge>
                  </div>
                </div>
                <CardHeader>
                  <CardTitle className="line-clamp-1">{gallery.title}</CardTitle>
                  <CardDescription className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {new Date(gallery.date_created).toLocaleDateString('pt-BR')}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {gallery.description || 'Sem descrição.'}
                  </p>
                </CardContent>
                <CardFooter className="border-t bg-muted/10 p-4">
                  <Button asChild className="w-full">
                    <Link to={`/gallery/${gallery.id}/view?token=${gallery.access_token}`}>
                      Acessar Galeria
                      <ChevronRight className="w-4 h-4 ml-2" />
                    </Link>
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
