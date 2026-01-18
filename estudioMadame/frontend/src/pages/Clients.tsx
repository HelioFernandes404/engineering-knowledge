import React from 'react';
import {
  Plus,
  ChevronDown,
  MoreHorizontal,
} from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

import { SearchFilterBar } from '@/components/SearchFilterBar';
import { ViewModeToggle } from '@/components/ViewModeToggle';
import { Pagination } from '@/components/Pagination';
import { useViewMode } from '@/hooks/useViewMode';
import { clientService } from '@/services/clientService';
import type { Client } from '@/types/client';
import { ClientDialog } from '@/components/ClientDialog';
import { format } from 'date-fns';

const Clients = () => {
  const { viewMode, setViewMode } = useViewMode('list');
  const [clients, setClients] = React.useState<Client[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [search, setSearch] = React.useState('');
  const [page, setPage] = React.useState(1);
  const [totalPages, setTotalPages] = React.useState(1);
  
  const [isDialogOpen, setIsDialogOpen] = React.useState(false);
  const [editingClient, setEditingClient] = React.useState<Client | undefined>();

  const fetchClients = React.useCallback(async () => {
    try {
      setLoading(true);
      const response = await clientService.list({ page, search, limit: 10 });
      setClients(response.data);
      if (response.meta) {
        setTotalPages(response.meta.total_pages);
      }
    } catch (error) {
      console.error('Failed to fetch clients:', error);
      toast.error('Failed to load clients');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  React.useEffect(() => {
    fetchClients();
  }, [fetchClients]);

  const handleCreateClient = async (values: any) => {
    try {
      await clientService.create(values);
      toast.success('Client created successfully');
      fetchClients();
    } catch (error) {
      console.error('Failed to create client:', error);
      toast.error('Failed to create client');
    }
  };

  const handleUpdateClient = async (values: any) => {
    if (!editingClient) return;
    try {
      await clientService.update(editingClient.id, values);
      toast.success('Client updated successfully');
      fetchClients();
    } catch (error) {
      console.error('Failed to update client:', error);
      toast.error('Failed to update client');
    }
  };

  const handleDeleteClient = async (id: string) => {
    if (!confirm('Are you sure you want to delete this client?')) return;
    try {
      await clientService.delete(id);
      toast.success('Client deleted successfully');
      fetchClients();
    } catch (error) {
      console.error('Failed to delete client:', error);
      toast.error('Failed to delete client');
    }
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase();
  };

  return (
    <div className="container max-w-7xl mx-auto px-6 pt-10">
      {/* Header */}
      <header className="flex flex-wrap items-center justify-between gap-4 mb-10">
        <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Clients</h1>
        <Button 
          className="gap-2 shadow-lg"
          onClick={() => {
            setEditingClient(undefined);
            setIsDialogOpen(true);
          }}
        >
          <Plus className="h-5 w-5" />
          <span className="font-medium tracking-wide">Add New Client</span>
        </Button>
      </header>

      {/* Search and Filters */}
      <SearchFilterBar
        searchPlaceholder="Search by client name or email..."
        onSearchChange={setSearch}
        filters={
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="gap-2">
                <span>All Clients</span>
                <ChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>All Clients</DropdownMenuItem>
              <DropdownMenuItem>Active Clients</DropdownMenuItem>
              <DropdownMenuItem>Inactive Clients</DropdownMenuItem>
              <DropdownMenuItem>New Clients (Last 30 days)</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        }
        actions={<ViewModeToggle viewMode={viewMode} onViewModeChange={setViewMode} />}
      />

      {/* Table */}
      <div className="border rounded-xl overflow-hidden bg-card">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead className="font-semibold">Client</TableHead>
              <TableHead className="font-semibold">Galleries</TableHead>
              <TableHead className="font-semibold text-center">Last Activity</TableHead>
              <TableHead className="w-16">
                <span className="sr-only">Actions</span>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">
                  Loading clients...
                </TableCell>
              </TableRow>
            ) : clients.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center text-muted-foreground">
                  No clients found.
                </TableCell>
              </TableRow>
            ) : (
              clients.map((client) => (
                <TableRow key={client.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <Avatar className="h-10 w-10">
                        <AvatarImage src={client.avatar} alt={client.name} />
                        <AvatarFallback>{getInitials(client.name)}</AvatarFallback>
                      </Avatar>
                      <div className="flex flex-col">
                        <p className="font-bold">{client.name}</p>
                        <p className="text-sm text-muted-foreground">{client.email}</p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="font-medium">{client.galleries_count}</TableCell>
                  <TableCell className="text-muted-foreground text-center">
                    {client.last_activity 
                      ? format(new Date(client.last_activity), 'MMM d, yyyy')
                      : 'No activity'}
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full hover:bg-muted">
                          <MoreHorizontal className="h-4 w-4 text-muted-foreground" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => {
                          setEditingClient(client);
                          setIsDialogOpen(true);
                        }}>
                          Edit Client
                        </DropdownMenuItem>
                        <DropdownMenuItem className="text-destructive" onClick={() => handleDeleteClient(client.id)}>
                          Delete Client
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <Pagination
          currentPage={page}
          totalPages={totalPages}
          onPageChange={setPage}
        />
      )}

      <ClientDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        onSubmit={editingClient ? handleUpdateClient : handleCreateClient}
        client={editingClient}
        title={editingClient ? 'Edit Client' : 'Add New Client'}
      />
    </div>
  );
};

export default Clients;
