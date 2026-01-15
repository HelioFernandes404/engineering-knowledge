import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from '@/components/Layout'
import Dashboard from '@/pages/Dashboard'
import Gallery from '@/pages/Gallery'
import Clients from '@/pages/Clients'
import Settings from '@/pages/Settings'
import CreateGallery from '@/pages/CreateGallery'
import GalleryDetail from '@/pages/GalleryDetail'
import GalleryLogin from '@/pages/GalleryLogin'
import ClientGallery from '@/pages/ClientGallery'
import Approvals from '@/pages/Approvals'
import Integrations from '@/pages/Integrations'
import Login from '@/pages/Login'
import ClientLogin from '@/pages/ClientLogin'
import ClientDashboard from '@/pages/ClientDashboard'
import ProtectedRoute from '@/components/ProtectedRoute'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/client/login" element={<ClientLogin />} />
        <Route path="/gallery/:id/login" element={<GalleryLogin />} />
        <Route path="/gallery/:id/view" element={<ClientGallery />} />

        {/* Client Protected Routes */}
        <Route path="/client/dashboard" element={
          <ProtectedRoute allowedRoles={['client']}>
            <ClientDashboard />
          </ProtectedRoute>
        } />

        {/* Admin Protected Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><Dashboard /></Layout>
          </ProtectedRoute>
        } />
        <Route path="/galleries" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><Gallery /></Layout>
          </ProtectedRoute>
        } />
        <Route path="/clients" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><Clients /></Layout>
          </ProtectedRoute>
        } />
        <Route path="/settings" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><Settings /></Layout>
          </ProtectedRoute>
        } />
        <Route path="/approvals" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><Approvals /></Layout>
          </ProtectedRoute>
        } />
        <Route path="/integrations" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><Integrations /></Layout>
          </ProtectedRoute>
        } />
        <Route path="/gallery/create" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><CreateGallery /></Layout>
          </ProtectedRoute>
        } />
        <Route path="/gallery/:id" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <Layout><GalleryDetail /></Layout>
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
