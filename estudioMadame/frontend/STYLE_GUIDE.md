# Guia de Estilo - Estúdio Madame

## 📋 Visão Geral
Este documento define os padrões de design e desenvolvimento para manter consistência visual em todas as páginas do projeto.

## 🎨 Paleta de Cores

O projeto usa o sistema de cores do shadcn/ui configurado em `src/index.css`:

### Cores Principais
- **Primary**: `oklch(0.577 0.245 27.325)` - Tom terracota/terra
- **Background**: `oklch(1 0 0)` - Branco puro
- **Foreground**: `oklch(0.141 0.005 285.823)` - Texto escuro
- **Muted**: `oklch(0.967 0.001 286.375)` - Cinza claro para backgrounds secundários

### Uso das Cores
```tsx
// Botão primário
<Button>Texto</Button>

// Texto com destaque primary
<p className="text-primary">Texto em destaque</p>

// Background muted para seções
<div className="bg-muted">...</div>
```

## 🔤 Tipografia

### Fontes
O projeto usa as fontes do sistema (sans-serif padrão). **NÃO use `font-serif`** - mantenha o padrão limpo e moderno.

```tsx
// Títulos principais
<h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
  Título Principal
</h1>

// Títulos de seção
<h2 className="text-3xl font-bold leading-[1.1]">
  Título de Seção
</h2>

// Texto normal
<p className="text-base">Texto comum</p>

// Texto muted
<p className="text-muted-foreground">Texto secundário</p>
```

### Hierarquia de Tamanhos
- **Hero Title**: `text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tighter`
- **Page Title**: `text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl`
- **Section Title**: `text-3xl font-bold leading-[1.1]`
- **Card Title**: `text-xl font-bold` ou `font-bold` (para componentes Card do shadcn)
- **Stats/Numbers**: `text-4xl font-bold`
- **Body Text**: `text-base` ou `text-lg`
- **Small Text**: `text-sm`
- **Muted Text**: `text-sm text-muted-foreground`

## 🧱 Componentes shadcn/ui

### Componentes Disponíveis
Use sempre os componentes do shadcn/ui localizados em `src/components/ui/`:

```tsx
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Input } from '@/components/ui/input'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
```

### Variantes de Botões
```tsx
<Button variant="default">Primary</Button>
<Button variant="outline">Secondary</Button>
<Button variant="ghost">Subtle</Button>
<Button variant="link">Link Style</Button>
```

### Cards Padrão
```tsx
<Card>
  <CardContent className="p-6">
    {/* Decorative background */}
    <div className="absolute -right-6 -top-6 w-24 h-24 bg-muted rounded-full opacity-50"></div>

    <div className="relative z-10">
      {/* Conteúdo */}
    </div>
  </CardContent>
</Card>
```

## 📐 Layout e Espaçamento

### Container Principal
```tsx
<main className="container max-w-7xl mx-auto px-6 pt-10">
  {/* Conteúdo */}
</main>
```

### Grid de Cards
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</div>
```

### Espaçamento Vertical
- Seção principal: `py-24 md:py-32`
- Entre elementos: `mb-8` ou `mb-10`
- Entre cards: `gap-4` ou `gap-6`

## 🎯 Navegação

### Navbar Padrão
```tsx
<nav className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
  <div className="container max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
    {/* Logo */}
    <div className="flex items-center gap-3">
      <span className="font-bold">Estúdio Madame</span>
    </div>

    {/* Navigation items */}
  </div>
</nav>
```

## 🎨 Efeitos e Transições

### Hover States
```tsx
// Cards com hover
<Card className="hover:shadow-md transition-shadow">

// Botões com hover
<Button className="hover:bg-primary/90 transition-colors">

// Links com hover
<a className="text-muted-foreground hover:text-foreground transition-colors">
```

### Animações de Imagem
```tsx
<img
  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
  src="..."
/>
```

## 📱 Responsividade

### Breakpoints Tailwind
- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px

### Padrões Responsivos
```tsx
// Flex direction
<div className="flex flex-col md:flex-row">

// Grid columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// Text size
<h1 className="text-4xl md:text-5xl lg:text-6xl">

// Spacing
<div className="px-4 md:px-6 lg:px-8">

// Hide/Show
<div className="hidden md:block">
<div className="md:hidden">
```

## 🌓 Dark Mode

O projeto suporta dark mode via `next-themes`. Use as classes do Tailwind normalmente:

```tsx
// As cores já se adaptam automaticamente
<div className="bg-background text-foreground">
<Card className="bg-card text-card-foreground">
```

## 📝 Checklist para Novas Páginas

Ao criar uma nova página, certifique-se de:

- [ ] Importar componentes de `@/components/ui/`
- [ ] **NÃO usar `font-serif`** - usar apenas `font-bold` com `tracking-tighter` para títulos
- [ ] Aplicar `container max-w-7xl mx-auto px-6` no main
- [ ] Usar cores do tema (`primary`, `muted`, `foreground`)
- [ ] Implementar responsividade mobile-first
- [ ] Adicionar estados hover e transições
- [ ] Testar no modo claro e escuro
- [ ] Manter consistência com navegação e footer

## 🔗 Exemplo de Estrutura de Página

```tsx
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

function NewPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
        {/* ... */}
      </nav>

      <main className="container max-w-7xl mx-auto px-6 pt-10">
        {/* Header */}
        <div className="mb-10">
          <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
            Título Principal
          </h1>
        </div>

        {/* Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              {/* ... */}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}

export default NewPage
```

## 📦 Estrutura de Arquivos

```
src/
├── components/
│   ├── ui/              # Componentes shadcn/ui
│   ├── theme-provider.tsx
│   └── mode-toggle.tsx
├── pages/
│   ├── Home.tsx         # Homepage
│   ├── Dashboard.tsx    # Dashboard
│   └── NewPage.tsx      # Nova página
├── lib/
│   └── utils.ts
├── App.tsx
└── index.css
```

## 🚀 Adicionando uma Nova Rota

1. Criar arquivo em `src/pages/NewPage.tsx`
2. Seguir o guia de estilo acima
3. Adicionar rota em `src/App.tsx`:

```tsx
import NewPage from '@/pages/NewPage'

// No componente App
<Route path="/new-page" element={<NewPage />} />
```

---

**Última atualização**: 2025-11-24
