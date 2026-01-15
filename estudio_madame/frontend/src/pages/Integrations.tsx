import { useState } from 'react';
import {
  PlugZap,
  FolderOutput,
  RefreshCw,
  RotateCw,
  Folder,
  FolderCheck,
  FolderPlus,
  ChevronRight,
  Search,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Separator } from '@/components/ui/separator';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { toast } from 'sonner';

// Mock folders data
const FOLDERS = [
  { id: 1, name: 'Client Albums', selected: false },
  { id: 2, name: 'Galleries', selected: true },
  { id: 3, name: 'Marketing Materials', selected: false },
  { id: 4, name: 'Presets & Actions', selected: false },
  { id: 5, name: 'Invoices & Contracts', selected: false },
  { id: 6, name: 'Archived Projects', selected: false },
  { id: 7, name: 'Wedding Photos', selected: false },
];

const Integrations = () => {
  const [isConnected, setIsConnected] = useState(true);
  const [autoSync, setAutoSync] = useState(true);
  const [lastSynced, setLastSynced] = useState('5 mins ago');
  const [selectedFolder, setSelectedFolder] = useState('/Estúdio Madame Backups/Galleries/');

  // Dialog states
  const [folderDialogOpen, setFolderDialogOpen] = useState(false);
  const [newFolderDialogOpen, setNewFolderDialogOpen] = useState(false);
  const [newFolderName, setNewFolderName] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const handleDisconnect = () => {
    setIsConnected(false);
    toast.success('Google Drive disconnected');
  };

  const handleConnect = () => {
    setIsConnected(true);
    toast.success('Google Drive connected successfully');
  };

  const handleSync = () => {
    setLastSynced('Just now');
    toast.success('Sync completed');
    setTimeout(() => setLastSynced('1 min ago'), 60000);
  };

  const handleAutoSyncToggle = (checked: boolean) => {
    setAutoSync(checked);
    toast.success(checked ? 'Auto-sync enabled' : 'Auto-sync disabled');
  };

  const handleSelectFolder = () => {
    const selectedFolderItem = FOLDERS.find(f => f.selected);
    if (selectedFolderItem) {
      setSelectedFolder(`/Estúdio Madame Backups/${selectedFolderItem.name}/`);
      toast.success(`Folder updated to ${selectedFolderItem.name}`);
    }
    setFolderDialogOpen(false);
  };

  const handleCreateFolder = () => {
    if (!newFolderName.trim()) {
      toast.error('Folder name cannot be empty');
      return;
    }
    toast.success(`Folder "${newFolderName}" created successfully`);
    setNewFolderName('');
    setNewFolderDialogOpen(false);
  };

  return (
    <>
      <div className="p-4 md:p-8">
        <div className="mx-auto max-w-4xl">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight">Google Drive Integration</h1>
            <p className="text-muted-foreground text-base mt-2">
              Connect your Google Drive account to seamlessly back up and sync your photo galleries.
            </p>
          </div>

          {/* Connection Status Card */}
          <Card className="mb-6">
            <CardContent className="p-6">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className="flex items-center justify-center h-12 w-12 rounded-lg bg-secondary">
                    <svg height="24" viewBox="0 0 48 48" width="24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M31.4,42.6l-6.8-11.8l-1.9,3.3l8.6,15C32,49.1,32.7,49,33.5,49H39l-7.6-13.2L31.4,42.6z" fill="#4CAF50"></path>
                      <path d="M16.6,5.4l6.8,11.8l1.9-3.3L16.7,0.9C16,0.9,15.3,1,14.5,1H9l7.6,13.2L16.6,5.4z" fill="#1E88E5"></path>
                      <path d="M43.4,29.4l-11.8,6.8l3.3,1.9L48.1,29.3c0-0.7-0.1-1.3-0.1-2H36l-1.9,3.3L43.4,29.4z" fill="#FFC107"></path>
                      <path d="M4.6,18.6l11.8-6.8l-3.3-1.9L0.9,18.7c0,0.7,0.1,1.3,0.1,2H12l1.9-3.3L4.6,18.6z" fill="#E53935"></path>
                      <path d="M15.1,16.5l-2.6,4.5l-7.9,0L1,27.3c0,0.7,0.1,1.4,0.3,2l11.2,0l2.6-4.5l7.9,0L26.7,18l-11.3,0L15.1,16.5z" fill="#2196F3"></path>
                      <path d="M32.9,31.5l2.6-4.5l7.9,0L47,20.7c0-0.7-0.1-1.4-0.3-2L35.5,18l-2.6,4.5l-7.9,0L21.3,30l11.3,0L32.9,31.5z" fill="#FBC02D"></path>
                    </svg>
                  </div>
                  <div>
                    <p className="text-lg font-bold tracking-tight">Connection Status</p>
                    <div className="flex items-center gap-2 mt-1">
                      <div className={`h-2 w-2 rounded-full ${isConnected ? 'bg-emerald-500' : 'bg-muted-foreground'}`}></div>
                      <p className="text-muted-foreground text-sm">
                        {isConnected ? 'Connected' : 'Not Connected'}
                      </p>
                    </div>
                    {isConnected && (
                      <div className="flex items-center gap-2 mt-2">
                        <p className="text-muted-foreground text-xs">
                          Last synced: {lastSynced}
                        </p>
                        <button
                          onClick={handleSync}
                          className="text-muted-foreground hover:text-primary cursor-pointer transition-colors"
                        >
                          <RotateCw className="h-4 w-4" />
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {isConnected ? (
                  <Button
                    variant="destructive"
                    className="w-full sm:w-auto gap-2"
                    onClick={handleDisconnect}
                  >
                    <PlugZap className="h-4 w-4" />
                    Disconnect
                  </Button>
                ) : (
                  <Button
                    className="w-full sm:w-auto gap-2"
                    onClick={handleConnect}
                  >
                    <PlugZap className="h-4 w-4" />
                    Connect to Google Drive
                  </Button>
                )}
              </div>

              <p className="text-muted-foreground text-xs mt-4">
                By connecting your account, you agree to our{' '}
                <a href="#" className="underline hover:text-primary">
                  Terms of Service
                </a>{' '}
                and{' '}
                <a href="#" className="underline hover:text-primary">
                  Privacy Policy
                </a>
                .
              </p>
            </CardContent>
          </Card>

          {/* Configuration Card */}
          <Card>
            <CardContent className="p-6">
              <div className="mb-6">
                <p className="text-lg font-bold tracking-tight">Configuration</p>
                <p className="text-muted-foreground text-base mt-1">
                  Setup your synchronization preferences once connected.
                </p>
              </div>

              <div className="space-y-6">
                {/* Destination Folder */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="flex items-start gap-4">
                    <FolderOutput className="h-5 w-5 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-base font-medium">Destination Folder</p>
                      <p className="text-muted-foreground text-sm">
                        {selectedFolder}
                      </p>
                    </div>
                  </div>
                  <Button
                    variant="secondary"
                    size="sm"
                    className="w-full sm:w-auto"
                    disabled={!isConnected}
                    onClick={() => setFolderDialogOpen(true)}
                  >
                    Change Folder
                  </Button>
                </div>

                <Separator />

                {/* Auto-sync Toggle */}
                <div className="flex items-center justify-between">
                  <div className="flex items-start gap-4">
                    <RefreshCw className="h-5 w-5 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-base font-medium">Auto-sync new galleries</p>
                      <p className="text-muted-foreground text-sm">
                        Automatically sync photos from new galleries.
                      </p>
                    </div>
                  </div>
                  <Switch
                    checked={autoSync}
                    onCheckedChange={handleAutoSyncToggle}
                    disabled={!isConnected}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Folder Selection Dialog */}
      <Dialog open={folderDialogOpen} onOpenChange={setFolderDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <div className="flex items-center justify-between">
              <div>
                <DialogTitle className="text-lg font-semibold">
                  Select Destination Folder
                </DialogTitle>
                <DialogDescription className="mt-1">
                  Choose a folder in your Google Drive to sync your galleries.
                </DialogDescription>
              </div>
              <Button
                variant="secondary"
                size="sm"
                className="gap-2"
                onClick={() => setNewFolderDialogOpen(true)}
              >
                <FolderPlus className="h-4 w-4" />
                New Folder
              </Button>
            </div>
          </DialogHeader>

          <div className="py-4">
            {/* Breadcrumb */}
            <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
              <Folder className="h-4 w-4 text-primary" />
              <a href="#" className="hover:text-primary transition-colors">
                My Drive
              </a>
              <ChevronRight className="h-4 w-4" />
              <a href="#" className="hover:text-primary transition-colors">
                Estúdio Madame Backups
              </a>
              <ChevronRight className="h-4 w-4" />
              <span className="font-medium text-foreground">Galleries</span>
            </div>

            {/* Search */}
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search folders..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Folder List */}
            <div className="border rounded-lg h-80 overflow-y-auto">
              <ul className="divide-y">
                {FOLDERS.filter((folder) =>
                  folder.name.toLowerCase().includes(searchQuery.toLowerCase())
                ).map((folder) => (
                  <li
                    key={folder.id}
                    className={`flex items-center gap-3 px-4 py-3 hover:bg-secondary/50 transition-colors cursor-pointer ${
                      folder.selected ? 'bg-secondary' : ''
                    }`}
                  >
                    {folder.selected ? (
                      <FolderCheck className="h-5 w-5 text-primary" />
                    ) : (
                      <Folder className="h-5 w-5 text-primary" />
                    )}
                    <span
                      className={`text-sm ${
                        folder.selected
                          ? 'text-primary font-semibold'
                          : 'text-foreground'
                      }`}
                    >
                      {folder.name}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <DialogFooter>
            <Button
              variant="secondary"
              onClick={() => setFolderDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button onClick={handleSelectFolder} className="font-bold tracking-tight">
              Select Folder
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* New Folder Dialog */}
      <Dialog open={newFolderDialogOpen} onOpenChange={setNewFolderDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-secondary">
                <FolderPlus className="h-6 w-6 text-primary" />
              </div>
              <div>
                <DialogTitle className="text-2xl font-bold tracking-tight">
                  Create New Folder
                </DialogTitle>
                <DialogDescription className="mt-1">
                  This will create a new folder in your Google Drive.
                </DialogDescription>
              </div>
            </div>
          </DialogHeader>

          <div className="py-3">
            <Label htmlFor="folder-name" className="text-base font-medium">
              Folder Name
            </Label>
            <Input
              id="folder-name"
              placeholder="Jane & John's Wedding"
              value={newFolderName}
              onChange={(e) => setNewFolderName(e.target.value)}
              className="mt-2 h-14 text-base"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleCreateFolder();
                }
              }}
            />
            <p className="text-muted-foreground text-sm mt-2">
              Tip: A clear name helps with organization.
            </p>
          </div>

          <DialogFooter>
            <Button
              variant="secondary"
              onClick={() => {
                setNewFolderDialogOpen(false);
                setNewFolderName('');
              }}
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreateFolder}
              className="font-bold tracking-tight"
            >
              Create
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default Integrations;
