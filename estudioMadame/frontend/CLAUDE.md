# Estúdio Madame - Frontend

## 📁 Estrutura do Projeto

Este projeto foi refatorado para seguir padrões modernos de organização e reutilização de código.

### Arquitetura

```
src/
├── components/          # Componentes reutilizáveis
│   ├── ui/             # Componentes shadcn/ui (60+ componentes)
│   ├── gallery/        # Componentes específicos de galeria
│   ├── forms/          # Componentes de formulário
│   ├── Layout.tsx      # Layout principal com sidebar
│   ├── StatusBadge.tsx # Badges de status (Gallery, Approval, Dashboard)
│   ├── Pagination.tsx  # Componente de paginação reutilizável
│   ├── ViewModeToggle.tsx      # Toggle grid/list view
│   ├── SearchFilterBar.tsx     # Barra de busca com filtros
│   └── BulkActionsBar.tsx      # Ações em lote com seleção
│
├── hooks/              # Custom hooks
│   ├── useMobile.ts    # Detecta tela mobile
│   ├── useSelection.ts # Gerencia seleção de múltiplos items
│   ├── useViewMode.ts  # Gerencia modo de visualização (grid/list)
│   ├── useSearch.ts    # Busca e filtro de items
│   ├── usePagination.ts # Lógica completa de paginação
│   └── useFilters.ts   # Filtros e ordenação genéricos
│
├── pages/              # Páginas da aplicação
│   ├── Home.tsx        # Landing page
│   ├── Dashboard.tsx   # Dashboard principal
│   ├── Gallery.tsx     # Lista de galerias
│   ├── GalleryDetail.tsx       # Detalhes da galeria
│   ├── CreateGallery.tsx       # Criar nova galeria
│   ├── Clients.tsx     # Gerenciamento de clientes
│   ├── Approvals.tsx   # Aprovações de clientes
│   ├── Settings.tsx    # Configurações
│   ├── Integrations.tsx # Integrações (Google Drive)
│   ├── ClientGallery.tsx       # Visualização do cliente
│   └── GalleryLogin.tsx        # Login para galeria
│
├── types/              # TypeScript types & interfaces
│   └── index.ts        # Gallery, Client, Approval, Photo, etc
│
├── utils/              # Funções utilitárias
│   └── status.ts       # Utilitários para status badges
│
├── constants/          # Constantes e mock data
│   └── mockData.ts     # Dados mockados centralizados
│
├── lib/                # Configurações e helpers
│   └── utils.ts        # Função cn() para className
│
└── App.tsx             # Rotas da aplicação
```

## 🎯 Componentes Reutilizáveis

### Componentes de UI Base

**StatusBadge** - Badges de status tipados para diferentes contextos
```tsx
import { GalleryStatusBadge, ApprovalStatusBadge, DashboardStatusBadge } from '@/components/StatusBadge';

<GalleryStatusBadge status="Published" />
<ApprovalStatusBadge status="complete" />
<DashboardStatusBadge status="Delivered" icon={<CheckCircle />} />
```

**Pagination** - Paginação com ellipsis automático
```tsx
import { Pagination } from '@/components/Pagination';

<Pagination
  currentPage={1}
  totalPages={10}
  onPageChange={(page) => console.log(page)}
/>
```

**ViewModeToggle** - Toggle entre visualização grid/list
```tsx
import { ViewModeToggle } from '@/components/ViewModeToggle';

<ViewModeToggle viewMode={viewMode} onViewModeChange={setViewMode} />
```

**SearchFilterBar** - Barra de busca com slots para filtros
```tsx
import { SearchFilterBar } from '@/components/SearchFilterBar';

<SearchFilterBar
  searchPlaceholder="Buscar..."
  onSearchChange={(value) => console.log(value)}
  filters={<DropdownMenu>...</DropdownMenu>}
  actions={<Button>Ação</Button>}
/>
```

**BulkActionsBar** - Ações em lote com checkbox "select all"
```tsx
import { BulkActionsBar } from '@/components/BulkActionsBar';

<BulkActionsBar
  selectedCount={5}
  selectAll={selectAll}
  onSelectAllChange={handleSelectAll}
  actions={<>
    <Button>Compartilhar</Button>
    <Button>Deletar</Button>
  </>}
/>
```

### Componentes de Galeria

**GalleryHeader** - Header com navegação e ações
```tsx
import { GalleryHeader } from '@/components/gallery/GalleryHeader';

<GalleryHeader
  title="Minha Galeria"
  status="published"
  onShare={handleShare}
  onPreview={handlePreview}
/>
```

**GalleryInfoCard** - Card de informações da galeria
```tsx
import { GalleryInfoCard } from '@/components/gallery/GalleryInfoCard';

<GalleryInfoCard
  coverImage="url"
  date="Oct 12, 2024"
  location="Berkshire"
  publicLink="retro.gallery/v/abc"
  onCopyLink={handleCopy}
/>
```

**GalleryStats** - Grid de estatísticas
```tsx
import { GalleryStats } from '@/components/gallery/GalleryStats';

<GalleryStats stats={[
  { label: 'Photos', value: 342, icon: Camera },
  { label: 'Views', value: 1205, icon: Eye }
]} />
```

**ClientSidebar** - Sidebar com detalhes do cliente
```tsx
import { ClientSidebar } from '@/components/gallery/ClientSidebar';

<ClientSidebar
  client={{
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    avatar: 'JD'
  }}
  onViewProfile={handleViewProfile}
/>
```

**PhotoGridView & PhotoListView** - Views de fotos
```tsx
import { PhotoGridView, PhotoListView } from '@/components/gallery';

<PhotoGridView photos={photos} onDelete={handleDelete} onEdit={handleEdit} />
<PhotoListView photos={photos} onDelete={handleDelete} />
```

### Componentes de Formulário

**FileUpload** - Upload de arquivo com preview
```tsx
import { FileUpload } from '@/components/forms/FileUpload';

<FileUpload
  label="Cover Image"
  preview={imagePreview}
  onFileSelect={handleFileSelect}
  onRemove={removeImage}
/>
```

**PrivacySelector** - Seletor de privacidade (Public/Private/Protected)
```tsx
import { PrivacySelector } from '@/components/forms/PrivacySelector';

<PrivacySelector value={privacy} onValueChange={setPrivacy} />
```

## 🪝 Custom Hooks

### useSelection
Gerencia seleção de múltiplos items com "select all"
```tsx
import { useSelection } from '@/hooks/useSelection';

const {
  items,
  selectAll,
  selectedCount,
  handleSelectAll,
  handleSelectItem,
  handleToggleItem,
  clearSelection
} = useSelection<Gallery>(MOCK_GALLERIES);
```

### useViewMode
Gerencia modo de visualização (grid/list)
```tsx
import { useViewMode } from '@/hooks/useViewMode';

const { viewMode, setViewMode, toggleViewMode, isGridView, isListView } = useViewMode('list');
```

### useSearch
Busca e filtro em arrays
```tsx
import { useSearch } from '@/hooks/useSearch';

const {
  searchQuery,
  filteredItems,
  handleSearch,
  clearSearch,
  hasResults
} = useSearch(items, ['name', 'email']);
```

### usePagination
Lógica completa de paginação
```tsx
import { usePagination } from '@/hooks/usePagination';

const {
  currentPage,
  totalPages,
  canGoNext,
  canGoPrevious,
  goToPage,
  nextPage,
  previousPage,
  paginateItems
} = usePagination({
  totalItems: 100,
  itemsPerPage: 10
});

const paginatedItems = paginateItems(allItems);
```

### useFilters
Filtros e ordenação genéricos
```tsx
import { useFilters } from '@/hooks/useFilters';

const {
  filters,
  filteredItems,
  setFilter,
  clearFilters,
  setSort,
  sortKey,
  sortDirection,
  activeFiltersCount
} = useFilters({
  items: galleries,
  initialFilters: { status: 'Published' },
  initialSort: { key: 'dateCreated', direction: 'desc' }
});
```

## 📦 Types & Constants

### Types Centralizados
```tsx
import type {
  Gallery,
  GalleryStatus,
  Client,
  Approval,
  ApprovalStatus,
  DashboardGallery,
  Photo
} from '@/types';
```

### Mock Data
```tsx
import {
  MOCK_GALLERIES,
  MOCK_CLIENTS,
  MOCK_APPROVALS,
  MOCK_DASHBOARD_GALLERIES
} from '@/constants/mockData';
```

### Utilitários de Status
```tsx
import {
  getGalleryStatusColor,
  getGalleryStatusDotColor,
  getApprovalStatusColor,
  getDashboardStatusVariant
} from '@/utils/status';
```

## 🎨 Padrões de Código

### 1. Separação de Responsabilidades
- **Components**: Apenas UI e comportamento visual
- **Hooks**: Lógica de negócio reutilizável
- **Utils**: Funções puras sem estado
- **Types**: Definições de tipos TypeScript
- **Constants**: Dados estáticos/mock

### 2. Composição sobre Duplicação
Prefira compor componentes pequenos ao invés de duplicar código.

**❌ Antes:**
```tsx
// Código duplicado em 3 arquivos
<div className="flex items-center rounded-lg border p-1">
  <Button variant={viewMode === 'grid' ? 'secondary' : 'ghost'} ...>
    <LayoutGrid />
  </Button>
  <Button variant={viewMode === 'list' ? 'secondary' : 'ghost'} ...>
    <List />
  </Button>
</div>
```

**✅ Depois:**
```tsx
// Componente reutilizável
<ViewModeToggle viewMode={viewMode} onViewModeChange={setViewMode} />
```

### 3. TypeScript Tipado
Use tipos fortes e evite `any`

**❌ Evite:**
```tsx
const data: any = ...
```

**✅ Prefira:**
```tsx
import type { Gallery } from '@/types';
const galleries: Gallery[] = ...
```

### 4. Custom Hooks para Lógica Compartilhada
Extraia lógica repetida em hooks reutilizáveis

**❌ Antes:**
```tsx
const [items, setItems] = useState(data);
const [selectAll, setSelectAll] = useState(false);
const selectedCount = items.filter(i => i.selected).length;
const handleSelectAll = (checked: boolean) => {
  setSelectAll(checked);
  setItems(items.map(i => ({ ...i, selected: checked })));
};
```

**✅ Depois:**
```tsx
const { items, selectAll, selectedCount, handleSelectAll } = useSelection(data);
```

## 🚀 Próximos Passos

### Melhorias Futuras
1. **API Integration**: Substituir mock data por chamadas reais
2. **State Management**: Adicionar Zustand/Context para estado global
3. **Testing**: Adicionar testes unitários com Vitest
4. **Code Splitting**: Implementar lazy loading das páginas
5. **Performance**: Adicionar React.memo em componentes pesados

### Estrutura Recomendada para Novos Componentes
```
src/components/feature-name/
├── FeatureComponent.tsx      # Componente principal
├── FeatureHeader.tsx          # Subcomponente
├── FeatureList.tsx            # Subcomponente
└── index.ts                   # Export barrel
```

### Padrão para Novos Hooks
```tsx
// src/hooks/useFeature.ts
import { useState, useCallback } from 'react';

export const useFeature = (initialValue: Type) => {
  const [state, setState] = useState(initialValue);

  const handler = useCallback(() => {
    // lógica
  }, []);

  return {
    state,
    handler,
    // helpers
  };
};
```

## 📚 Bibliotecas Principais

- **React 19** - Framework UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool
- **Tailwind CSS 4** - Styling
- **shadcn/ui** - Componentes base
- **Lucide React** - Ícones
- **React Router** - Roteamento
- **Sonner** - Notificações toast
- **Next Themes** - Dark mode

## 🔧 Comandos

```bash
# Desenvolvimento
npm run dev

# Build
npm run build

# Preview da build
npm run preview

# Lint
npm run lint
```

## 📝 Notas de Refatoração

Esta refatoração focou em:
- ✅ Eliminar código duplicado
- ✅ Criar componentes reutilizáveis
- ✅ Extrair lógica em custom hooks
- ✅ Centralizar tipos e constantes
- ✅ Melhorar legibilidade
- ✅ Facilitar manutenção

**Redução de linhas:**
- GalleryDetail.tsx: 396 → 185 LOC (-53%)
- Gallery.tsx: código mais limpo
- Clients.tsx: código mais limpo

**Componentes criados:** 16
**Hooks criados:** 5
**Build:** ✅ Passando sem erros
