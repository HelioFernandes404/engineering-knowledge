import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import {
  Camera,
  Users,
  HardDrive,
  Plus,
  CheckCircle2,
  Clock,
  UploadCloud,
  Image as ImageIcon,
} from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { DashboardStatusBadge } from '@/components/StatusBadge';
import { dashboardService } from "@/services/dashboardService";
import type { DashboardStats, DashboardGallery } from '@/services/dashboardService';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('all');
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [galleries, setGalleries] = useState<DashboardGallery[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const [statsRes, galleriesRes] = await Promise.all([
        dashboardService.getStats(),
        dashboardService.getRecentGalleries({ status_filter: activeTab })
      ]);
      setStats(statsRes.data);
      setGalleries(galleriesRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  }, [activeTab]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const statCards = [
    {
      label: "Active Galleries",
      value: stats?.active_galleries.toString() || "0",
      icon: <Camera className="h-6 w-6 text-primary" />,
      change: "From all clients",
      trend: "neutral"
    },
    {
      label: "Total Clients",
      value: stats?.total_clients.toString() || "0",
      icon: <Users className="h-6 w-6 text-chart-2" />,
      change: "Registered in system",
      trend: "neutral"
    },
    {
      label: "Storage Used",
      value: `${stats?.storage_percentage || 0}%`,
      icon: <HardDrive className="h-6 w-6 text-foreground" />,
      change: `${stats ? formatBytes(stats.storage_used_bytes) : '0 B'} / ${stats ? formatBytes(stats.storage_total_bytes) : '100 GB'}`,
      trend: (stats?.storage_percentage || 0) > 80 ? "warning" : "neutral"
    }
  ];

  function formatBytes(bytes: number, decimals = 2) {
    if (!+bytes) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
  }

  const getStatusIcon = (status: DashboardGallery['status']) => {
    switch (status) {
      case 'Delivered': return <CheckCircle2 className="h-3.5 w-3.5 mr-1" />;
      case 'Editing': return <Clock className="h-3.5 w-3.5 mr-1" />;
      case 'Uploading': return <UploadCloud className="h-3.5 w-3.5 mr-1" />;
      case 'Selection': return <ImageIcon className="h-3.5 w-3.5 mr-1" />;
    }
  };

  return (
    <div className="container max-w-7xl mx-auto px-4 md:px-6 py-8">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
        <div>
          <h2 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Dashboard Overview</h2>
        </div>

        <Link to="/gallery/create">
          <Button className="gap-2 shadow-lg">
            <Plus className="h-5 w-5" />
            <span className="font-medium tracking-wide">Create New Gallery</span>
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {statCards.map((stat, index) => (
          <Card key={index} className="relative overflow-hidden group hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="absolute -right-6 -top-6 w-24 h-24 bg-muted rounded-full opacity-50 group-hover:opacity-70 transition-opacity"></div>
              <div className="relative z-10 flex justify-between items-start mb-4">
                <div className="p-3 bg-muted rounded-lg">{stat.icon}</div>
                <Badge variant={stat.trend === 'warning' ? 'destructive' : 'secondary'} className="text-xs">
                  {stat.change}
                </Badge>
              </div>
              <h3 className="text-muted-foreground text-sm font-medium uppercase tracking-wider mb-1">{stat.label}</h3>
              <p className="text-4xl font-bold">{stat.value}</p>
              {stat.label === "Storage Used" && (
                <Progress value={stats?.storage_percentage || 0} className="mt-4" />
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Galleries Section */}
      <Card>
        <CardContent className="p-6 md:p-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <h3 className="text-2xl font-bold">Recent Galleries</h3>
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full md:w-auto">
              <TabsList className="grid grid-cols-3 w-full md:w-[300px]">
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="editing">Editing</TabsTrigger>
                <TabsTrigger value="delivered">Delivered</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {loading ? (
              <div className="h-40 flex items-center justify-center text-muted-foreground">Loading galleries...</div>
            ) : galleries.length === 0 ? (
              <div className="h-40 flex items-center justify-center text-muted-foreground">No galleries found.</div>
            ) : (
              galleries.map((gallery) => (
                <div 
                  key={gallery.id} 
                  className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-xl border bg-card hover:shadow-sm transition-all group"
                >
                  <div className="flex items-center gap-4 mb-4 sm:mb-0">
                    <div className="h-12 w-12 rounded-lg overflow-hidden bg-muted flex-shrink-0">
                      {gallery.image ? (
                        <img src={gallery.image} alt={gallery.title} className="h-full w-full object-cover" />
                      ) : (
                        <div className="h-full w-full flex items-center justify-center"><ImageIcon className="h-6 w-6 text-muted-foreground" /></div>
                      )}
                    </div>
                    <div>
                      <h4 className="font-bold group-hover:text-primary transition-colors">{gallery.title}</h4>
                      <div className="flex items-center text-xs text-muted-foreground mt-0.5">
                        <span>{gallery.date}</span>
                        <span className="mx-2">•</span>
                        <span>{gallery.photos} photos</span>
                        <span className="mx-2">•</span>
                        <span>{gallery.size}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
                    <DashboardStatusBadge status={gallery.status}>
                      <div className="flex items-center">
                        {getStatusIcon(gallery.status)}
                        {gallery.status}
                      </div>
                    </DashboardStatusBadge>
                    <Link to={`/gallery/${gallery.id}`}>
                      <Button variant="ghost" size="sm" className="text-xs font-semibold">Manage</Button>
                    </Link>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="mt-8 text-center">
            <Link to="/galleries">
              <Button variant="outline" className="font-medium">View All Galleries</Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
