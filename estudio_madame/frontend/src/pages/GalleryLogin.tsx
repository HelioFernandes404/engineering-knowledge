import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Mail, Lock, AlertCircle, AlertTriangle } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { authService } from '@/services/authService';
import { galleryService } from '@/services/galleryService';
import type { Gallery } from '@/types';

const GalleryLogin = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<'invalid' | 'expired' | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [gallery, setGallery] = useState<Gallery | null>(null);

  useEffect(() => {
    const fetchGallery = async () => {
      if (!id) return;
      try {
        const response = await galleryService.get(id);
        setGallery(response.data);
      } catch (err) {
        console.error('Failed to fetch gallery:', err);
        setError('expired');
      }
    };

    fetchGallery();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    
    setError(null);
    setIsLoading(true);

    try {
      // 1. Client login
      const loginResponse = await authService.clientLogin({ email, password });
      
      // Store user info and token
      localStorage.setItem('access_token', loginResponse.data.access_token);
      localStorage.setItem('client', JSON.stringify(loginResponse.data.client));
      localStorage.removeItem('user');

      // 2. Get gallery access token
      const accessResponse = await authService.getGalleryAccess(id);
      localStorage.setItem(`gallery_access_${id}`, accessResponse.data.gallery_access_token);

      // Success - redirect to client gallery view
      navigate(`/gallery/${id}/view`);
    } catch (err: any) {
      console.error('Login failed:', err);
      setError('invalid');
    } finally {
      setIsLoading(false);
    }
  };

  if (!gallery && !error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="h-8 w-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const coverImage = gallery?.cover_image || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=2000';

  return (
    <div className="min-h-screen w-full bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 bg-card rounded-2xl shadow-2xl overflow-hidden border">

          {/* Left Side - Large Image */}
          <div className="relative h-64 lg:h-auto lg:min-h-[600px]">
            <img
              src={coverImage}
              alt="Gallery cover"
              className="absolute inset-0 w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent lg:hidden" />

            <div className="absolute top-6 left-6 lg:hidden">
              <h2 className="text-xl font-bold text-white drop-shadow-lg">
                Estúdio Madame
              </h2>
            </div>
          </div>

          {/* Right Side - Login Form */}
          <div className="p-8 md:p-12 lg:p-16 flex flex-col justify-center">
            <div className="mb-8 text-center hidden lg:block">
              <h2 className="text-2xl font-bold tracking-tight text-primary">
                Estúdio Madame
              </h2>
            </div>

            <div className="mb-8">
              <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-2">
                {gallery?.title || 'Gallery Access'}
              </h1>
              <p className="text-muted-foreground text-base">
                {gallery?.event_date ? new Date(gallery.event_date).toLocaleDateString() : ''}. Please use the credentials provided by your photographer to access your photos.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-base font-medium">
                  Email
                </Label>
                <div className="relative">
                  <Input
                    id="email"
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="h-12 pr-12 text-base"
                    required
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <Mail className="h-5 w-5 text-muted-foreground" />
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-base font-medium">
                  Password
                </Label>
                <div className="relative">
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="h-12 pr-12 text-base"
                    required
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <Lock className="h-5 w-5 text-muted-foreground" />
                  </div>
                </div>
              </div>

              {error === 'invalid' && (
                <Alert variant="destructive" className="border-destructive/50 bg-destructive/10">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    Invalid email or password. Please try again.
                  </AlertDescription>
                </Alert>
              )}

              {error === 'expired' && (
                <Alert className="border-yellow-500/50 bg-yellow-500/10 text-yellow-600 dark:text-yellow-400">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    This gallery does not exist or has expired.
                  </AlertDescription>
                </Alert>
              )}

              <Button
                type="submit"
                className="w-full h-12 text-base font-bold"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
                    Signing in...
                  </>
                ) : (
                  'SIGN IN'
                )}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm text-muted-foreground">
              <p>
                Need help?{' '}
                <a href="#" className="text-primary hover:underline font-medium">
                  Contact Photographer
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GalleryLogin;
