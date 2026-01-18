import type { ReactNode } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  LayoutGrid,
  Image as ImageIcon,
  CheckCircle,
  Users,
  Settings as SettingsIcon,
  LifeBuoy,
  LogOut,
  PlugZap,
  Bell,
  Search,
  Menu,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet';
import { toast } from 'sonner';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const isActive = (path: string) => location.pathname === path;

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    toast.success('Sessão encerrada');
    navigate('/login');
  };

  const SidebarContent = () => (
    <div className="flex h-full flex-col justify-between">
      {/* Top Section */}
      <div className="flex flex-col gap-6">
        {/* Logo / Brand */}
        <div className="flex items-center gap-3">
          <Avatar className="h-10 w-10">
            <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name || 'User'}`} />
            <AvatarFallback>{user.name?.substring(0, 2).toUpperCase() || 'EM'}</AvatarFallback>
          </Avatar>
          <div className="flex flex-col">
            <h1 className="text-base font-medium">Estúdio Madame</h1>
            <p className="text-sm text-muted-foreground truncate max-w-[150px]">{user.email}</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex flex-col gap-2">
          <Link
            to="/dashboard"
            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive('/dashboard') ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-secondary/50 hover:text-foreground'}`}
          >
            <LayoutGrid className={`h-4 w-4 ${isActive('/dashboard') ? 'text-primary' : ''}`} />
            <span className={`text-sm font-medium ${isActive('/dashboard') ? 'text-primary' : ''}`}>
              Dashboard
            </span>
          </Link>
          <Link
            to="/galleries"
            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive('/galleries') ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-secondary/50 hover:text-foreground'}`}
          >
            <ImageIcon className={`h-4 w-4 ${isActive('/galleries') ? 'text-primary' : ''}`} />
            <span className={`text-sm font-medium ${isActive('/galleries') ? 'text-primary' : ''}`}>
              Galleries
            </span>
          </Link>
          <Link
            to="/approvals"
            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive('/approvals') ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-secondary/50 hover:text-foreground'}`}
          >
            <CheckCircle className={`h-4 w-4 ${isActive('/approvals') ? 'text-primary' : ''}`} />
            <span className={`text-sm font-medium ${isActive('/approvals') ? 'text-primary' : ''}`}>
              Approvals
            </span>
          </Link>
          <Link
            to="/clients"
            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive('/clients') ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-secondary/50 hover:text-foreground'}`}
          >
            <Users className={`h-4 w-4 ${isActive('/clients') ? 'text-primary' : ''}`} />
            <span className={`text-sm font-medium ${isActive('/clients') ? 'text-primary' : ''}`}>
              Clients
            </span>
          </Link>
          <Link
            to="/settings"
            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive('/settings') ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-secondary/50 hover:text-foreground'}`}
          >
            <SettingsIcon className={`h-4 w-4 ${isActive('/settings') ? 'text-primary' : ''}`} />
            <span className={`text-sm font-medium ${isActive('/settings') ? 'text-primary' : ''}`}>
              Settings
            </span>
          </Link>
          <Link
            to="/integrations"
            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive('/integrations') ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-secondary/50 hover:text-foreground'}`}
          >
            <PlugZap className={`h-4 w-4 ${isActive('/integrations') ? 'text-primary' : ''}`} />
            <span className={`text-sm font-medium ${isActive('/integrations') ? 'text-primary' : ''}`}>
              Integrations
            </span>
          </Link>
        </nav>
      </div>

      {/* Bottom Section */}
      <div className="flex flex-col gap-1">
        <Link
          to="#"
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-muted-foreground hover:bg-secondary/50 hover:text-foreground transition-colors"
        >
          <LifeBuoy className="h-4 w-4" />
          <span className="text-sm font-medium">Help</span>
        </Link>
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-muted-foreground hover:bg-secondary/50 hover:text-foreground transition-colors w-full text-left"
        >
          <LogOut className="h-4 w-4" />
          <span className="text-sm font-medium">Logout</span>
        </button>
        <Separator className="my-3" />
        <Button className="w-full font-bold tracking-tight">
          Upgrade Plan
        </Button>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen bg-background">
      {/* Desktop Sidebar */}
      <aside className="w-64 border-r bg-card p-4 hidden lg:flex flex-col">
        <SidebarContent />
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Navbar */}
        <nav className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="px-4 md:px-6 py-4 flex justify-between items-center">
            <div className="flex items-center gap-3">
              {/* Mobile Menu Button */}
              <Sheet>
                <SheetTrigger asChild className="lg:hidden">
                  <Button variant="ghost" size="icon">
                    <Menu className="h-5 w-5" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="w-64 p-4">
                  <SheetHeader>
                    <SheetTitle>Navigation Menu</SheetTitle>
                    <SheetDescription className="sr-only">
                      Access different sections of the Estúdio Madame administrative panel.
                    </SheetDescription>
                  </SheetHeader>
                  <SidebarContent />
                </SheetContent>
              </Sheet>

              <span className="font-bold hidden lg:block">Estúdio Madame</span>
            </div>

            <div className="flex items-center gap-6">
              <div className="hidden md:flex relative">
                <Input
                  type="text"
                  placeholder="Search galleries..."
                  className="pl-10 pr-4 w-64 rounded-full"
                />
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
              </div>

              <Button variant="ghost" size="icon" className="relative rounded-full">
                <Bell className="h-5 w-5" />
                <span className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full"></span>
              </Button>

              <Separator orientation="vertical" className="h-8 hidden md:block" />

              <div className="flex items-center gap-3">
                <Avatar className="h-9 w-9">
                  <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name || 'User'}`} alt="User" />
                  <AvatarFallback>{user.name?.substring(0, 2).toUpperCase() || 'SJ'}</AvatarFallback>
                </Avatar>
                <div className="hidden md:block">
                  <p className="text-sm font-bold leading-none">{user.name}</p>
                  <p className="text-xs text-muted-foreground mt-1">{user.role}</p>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Page Content */}
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
