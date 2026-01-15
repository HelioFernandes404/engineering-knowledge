import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  PlusCircle,
  Search,
  ListFilter,
  CalendarDays,
  ArrowUpDown,
  ChevronDown,
  Eye,
  Download,
  MessageSquare,
  Send,
  Loader2,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { ApprovalStatusBadge } from '@/components/StatusBadge';
import { approvalService } from '@/services/approvalService';
import type { Approval } from '@/services/approvalService';

const Approvals = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchApprovals = async () => {
      setIsLoading(true);
      try {
        const response = await approvalService.list({ search: searchQuery });
        setApprovals(response.data);
      } catch (error) {
        console.error('Failed to fetch approvals:', error);
      } finally {
        setIsLoading(false);
      }
    };

    const timer = setTimeout(() => {
      fetchApprovals();
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const getActionButton = (status: string) => {
    switch (status) {
      case 'complete':
        return (
          <Button variant="secondary" size="sm" className="gap-2">
            <Download className="h-4 w-4" />
            Export
          </Button>
        );
      case 'changes':
        return (
          <Button size="sm" className="gap-2">
            <MessageSquare className="h-4 w-4" />
            Feedback
          </Button>
        );
      case 'awaiting':
      default:
        return (
          <Button variant="secondary" size="sm" className="gap-2">
            <Send className="h-4 w-4" />
            Remind
          </Button>
        );
    }
  };

  return (
    <div className="p-4 md:p-8">
        <div className="mx-auto flex w-full max-w-7xl flex-col gap-8">
          {/* Header */}
          <div className="flex flex-col gap-6">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex flex-col gap-2">
                <h1 className="text-4xl font-bold tracking-tight">Client Approvals</h1>
                <p className="text-muted-foreground text-base">
                  Manage and track all your client photo selections and approvals.
                </p>
              </div>
              <Link to="/gallery/create">
                <Button className="gap-2">
                  <PlusCircle className="h-4 w-4" />
                  New Gallery
                </Button>
              </Link>
            </div>

            {/* Search and Filters */}
            <div className="flex flex-wrap items-center gap-2">
              <div className="relative flex-1 min-w-[320px]">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <Input
                  className="pl-12 h-10"
                  placeholder="Search by client or gallery..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>

              <div className="flex items-center gap-2">
                <Button variant="outline" className="gap-2">
                  <ListFilter className="h-4 w-4" />
                  Status
                  <ChevronDown className="h-4 w-4" />
                </Button>
                <Button variant="outline" className="gap-2">
                  <CalendarDays className="h-4 w-4" />
                  Date Range
                  <ChevronDown className="h-4 w-4" />
                </Button>
                <Button variant="outline" className="gap-2">
                  <ArrowUpDown className="h-4 w-4" />
                  Sort By
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          <Separator />

          {/* Approvals List */}
          <div className="flex flex-col gap-3">
            {isLoading ? (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : approvals.length > 0 ? (
              approvals.map((approval) => (
                <div
                  key={approval.id}
                  className="flex flex-col sm:flex-row items-center justify-between gap-4 rounded-xl border bg-card p-4 hover:border-primary/50 transition-colors"
                >
                  {/* Left Section - Client Info */}
                  <div className="flex w-full flex-1 items-center gap-4">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={approval.client_avatar} />
                      <AvatarFallback>{approval.client_name?.[0] || '?'}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <h3 className="text-base font-bold">
                        {approval.client_name} - {approval.gallery_name}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        Selection: {approval.selected_count} / {approval.total_count}
                      </p>
                    </div>
                  </div>

                  {/* Right Section - Status & Actions */}
                  <div className="flex w-full sm:w-auto items-center justify-between sm:justify-end gap-4">
                    <ApprovalStatusBadge status={approval.status as any} />

                    <div className="flex items-center gap-2">
                      <Link to={`/gallery/${approval.gallery_id}`}>
                        <Button variant="outline" size="icon" className="h-9 w-9">
                          <Eye className="h-4 w-4" />
                        </Button>
                      </Link>
                      {getActionButton(approval.status)}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="flex flex-col items-center justify-center py-20 text-center">
                <p className="text-muted-foreground">No approvals found.</p>
              </div>
            )}
          </div>
        </div>
    </div>
  );
};

export default Approvals;
