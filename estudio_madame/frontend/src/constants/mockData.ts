import type { Gallery, Approval, DashboardGallery, Client } from '@/types';

/**
 * Mock Galleries Data
 */
export const MOCK_GALLERIES: Gallery[] = [
  {
    id: '1',
    title: 'Johnson Wedding',
    client_id: '1',
    client_name: 'The Johnsons',
    date_created: 'Oct 12, 2023',
    status: 'published',
    photo_count: 350,
    cover_image: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=200',
    auto_sync_enabled: true,
    sync_status: 'idle',
  },
  {
    id: '2',
    title: 'Autumn Portraits 2023',
    client_id: '2',
    client_name: 'Multiple Clients',
    date_created: 'Sep 28, 2023',
    status: 'draft',
    photo_count: 120,
    cover_image: 'https://images.unsplash.com/photo-1469334031218-e382a71b716b?auto=format&fit=crop&q=80&w=200',
    auto_sync_enabled: false,
    sync_status: 'idle',
  },
  {
    id: '3',
    title: 'Miller Family Shoot',
    client_id: '3',
    client_name: 'The Millers',
    date_created: 'Sep 15, 2023',
    status: 'client_selection',
    photo_count: 215,
    cover_image: 'https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&q=80&w=200',
    auto_sync_enabled: true,
    sync_status: 'idle',
  },
  {
    id: '4',
    title: 'Cityscape Vol. II',
    client_id: '4',
    client_name: 'Personal Project',
    date_created: 'Aug 2, 2023',
    status: 'archived',
    photo_count: 88,
    cover_image: 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&q=80&w=200',
    auto_sync_enabled: false,
    sync_status: 'idle',
  },
];

/**
 * Mock Approvals Data
 */
export const MOCK_APPROVALS: Approval[] = [
  {
    id: '1',
    client_id: '1',
    client_name: 'Alice Chen',
    gallery_id: '1',
    gallery_name: 'Chen Wedding',
    client_avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alice',
    selected_count: 85,
    total_count: 200,
    status: 'complete',
    updated_at: 'Oct 12, 2023',
  },
  {
    id: '2',
    client_id: '2',
    client_name: 'Mark Carter',
    gallery_id: '2',
    gallery_name: 'Carter Family Portraits',
    client_avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Mark',
    selected_count: 112,
    total_count: 150,
    status: 'changes',
    updated_at: 'Oct 12, 2023',
  },
  {
    id: '3',
    client_id: '3',
    client_name: 'Vogue Magazine',
    gallery_id: '3',
    gallery_name: 'Desert Bloom Editorial',
    client_avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Vogue',
    selected_count: 0,
    total_count: 300,
    status: 'awaiting',
    updated_at: 'Oct 12, 2023',
  },
  {
    id: '4',
    client_id: '4',
    client_name: 'Sarah Goldberg',
    gallery_id: '4',
    gallery_name: 'Goldberg Graduation',
    client_avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah',
    selected_count: 45,
    total_count: 50,
    status: 'awaiting',
    updated_at: 'Oct 12, 2023',
  },
];

/**
 * Mock Dashboard Galleries Data
 */
export const MOCK_DASHBOARD_GALLERIES: DashboardGallery[] = [
  {
    id: '1',
    title: "Wedding: Elena & Marco",
    date: "Oct 24, 2023",
    image: "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=200",
    status: "Delivered",
    photos: 450,
    size: "2.4 GB"
  },
  {
    id: '2',
    title: "Autumn Editorial",
    date: "Nov 02, 2023",
    image: "https://images.unsplash.com/photo-1469334031218-e382a71b716b?auto=format&fit=crop&q=80&w=200",
    status: "Editing",
    photos: 128,
    size: "1.1 GB"
  },
  {
    id: '3',
    title: "Baby Luca Newborn",
    date: "Nov 10, 2023",
    image: "https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&q=80&w=200",
    status: "Uploading",
    photos: 85,
    size: "850 MB"
  },
  {
    id: '4',
    title: "Vintage Car Collection",
    date: "Nov 12, 2023",
    image: "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&q=80&w=200",
    status: "Selection",
    photos: 210,
    size: "1.8 GB"
  },
];

/**
 * Mock Clients Data
 */
export const MOCK_CLIENTS: Client[] = [
  {
    id: '1',
    name: 'Olivia Martin',
    email: 'olivia.martin@email.com',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=200',
    galleries_count: 5,
    last_activity: '2023-10-10T10:00:00Z',
    created_at: '2023-01-01T10:00:00Z',
    updated_at: '2023-10-10T10:00:00Z',
  },
  {
    id: '2',
    name: 'Jackson Lee',
    email: 'jackson.lee@email.com',
    avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&q=80&w=200',
    galleries_count: 3,
    last_activity: '2023-10-05T10:00:00Z',
    created_at: '2023-01-05T10:00:00Z',
    updated_at: '2023-10-05T10:00:00Z',
  },
  {
    id: '3',
    name: 'Isabella Nguyen',
    email: 'isabella.nguyen@email.com',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&q=80&w=200',
    galleries_count: 8,
    last_activity: '2023-09-20T10:00:00Z',
    created_at: '2023-01-10T10:00:00Z',
    updated_at: '2023-09-20T10:00:00Z',
  },
  {
    id: '4',
    name: 'William Kim',
    email: 'william.kim@email.com',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200',
    galleries_count: 1,
    last_activity: '2023-09-15T10:00:00Z',
    created_at: '2023-02-01T10:00:00Z',
    updated_at: '2023-09-15T10:00:00Z',
  },
  {
    id: '5',
    name: 'Sophia Garcia',
    email: 'sophia.garcia@email.com',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200',
    galleries_count: 12,
    last_activity: '2023-08-10T10:00:00Z',
    created_at: '2023-02-15T10:00:00Z',
    updated_at: '2023-08-10T10:00:00Z',
  },
];
