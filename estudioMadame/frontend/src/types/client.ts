export interface Client {
  id: string;
  name: string;
  email: string;
  phone?: string;
  avatar?: string;
  galleries_count: number;
  last_activity?: string;
  created_at: string;
  updated_at: string;
}

export interface ClientCreate {
  name: string;
  email: string;
  password?: string;
  phone?: string;
  avatar?: string;
}

export interface ClientUpdate {
  name?: string;
  email?: string;
  password?: string;
  phone?: string;
  avatar?: string;
}
