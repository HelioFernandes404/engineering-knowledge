import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

interface ProtectedRouteProps {
  children: ReactNode;
  allowedRoles?: ('admin' | 'client')[];
}

export default function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const token = localStorage.getItem('access_token');
  const userStr = localStorage.getItem('user');
  const clientStr = localStorage.getItem('client');
  const location = useLocation();

  if (!token) {
    // If it's a client route, redirect to client login
    if (location.pathname.startsWith('/client')) {
      return <Navigate to="/client/login" replace />;
    }
    return <Navigate to="/login" replace />;
  }

  const user = userStr ? JSON.parse(userStr) : null;
  const client = clientStr ? JSON.parse(clientStr) : null;
  
  // Determine current role
  const role = client ? 'client' : (user ? 'admin' : null);

  if (allowedRoles && role && !allowedRoles.includes(role as any)) {
    // Redirect to their respective dashboard if they don't have access
    if (role === 'admin') return <Navigate to="/dashboard" replace />;
    if (role === 'client') return <Navigate to="/client/dashboard" replace />;
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
