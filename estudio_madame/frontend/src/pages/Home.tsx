import { Button } from "@/components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ModeToggle } from "@/components/mode-toggle"

function Home() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 max-w-screen-2xl items-center">
          <div className="mr-4 flex">
            <a className="mr-6 flex items-center space-x-2" href="/">
              <span className="font-bold">Estúdio Madame</span>
            </a>
          </div>
          <div className="flex flex-1 items-center justify-end space-x-2">
            <nav className="flex items-center space-x-4">
              <Button variant="ghost">Serviços</Button>
              <Button variant="ghost">Portfolio</Button>
              <Button variant="ghost">Sobre</Button>
              <Button>Agendar</Button>
              <ModeToggle />
            </nav>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container flex flex-col items-center gap-4 py-24 md:py-32">
        <Badge variant="secondary" className="mb-4">
          📸 Fotografia Profissional
        </Badge>
        <h1 className="text-center text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
          Capture momentos
          <br />
          <span className="text-muted-foreground">inesquecíveis</span>
        </h1>
        <p className="max-w-[700px] text-center text-lg text-muted-foreground sm:text-xl">
          Fotografia profissional para ensaios, eventos e momentos especiais.
          Transformamos suas memórias em arte.
        </p>
        <div className="flex gap-4 mt-8">
          <Button size="lg" className="gap-2">
            Solicitar Orçamento
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="m9 18 6-6-6-6" />
            </svg>
          </Button>
          <Button size="lg" variant="outline">
            Ver Portfolio
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="container py-24 md:py-32">
        <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
          <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
            Serviços de Fotografia
          </h2>
          <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
            Oferecemos fotografia profissional para diversos tipos de ocasiões
          </p>
        </div>
        <div className="mx-auto grid justify-center gap-4 sm:grid-cols-2 md:max-w-[64rem] md:grid-cols-3 mt-12">
          <Card>
            <CardHeader>
              <CardTitle>Ensaios Fotográficos</CardTitle>
              <CardDescription>
                Ensaios individuais, em casal, família e gestante. Registros naturais e espontâneos
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Eventos</CardTitle>
              <CardDescription>
                Cobertura completa de casamentos, formaturas, aniversários e eventos corporativos
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Fotografia de Produtos</CardTitle>
              <CardDescription>
                Fotos profissionais para e-commerce, catálogos e divulgação de produtos
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-y border-border bg-muted/50">
        <div className="container grid gap-8 py-16 md:grid-cols-3">
          <div className="flex flex-col items-center text-center">
            <div className="text-4xl font-bold">300+</div>
            <div className="text-muted-foreground">Ensaios Realizados</div>
          </div>
          <div className="flex flex-col items-center text-center">
            <div className="text-4xl font-bold">5 anos</div>
            <div className="text-muted-foreground">De Experiência</div>
          </div>
          <div className="flex flex-col items-center text-center">
            <div className="text-4xl font-bold">100%</div>
            <div className="text-muted-foreground">Clientes Satisfeitos</div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container py-24 md:py-32">
        <div className="mx-auto flex max-w-[58rem] flex-col items-center justify-center gap-4 text-center">
          <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
            Pronto para eternizar seus momentos?
          </h2>
          <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
            Entre em contato e solicite um orçamento personalizado para seu projeto
          </p>
          <div className="flex gap-4 mt-4">
            <Button size="lg">Solicitar Orçamento</Button>
            <Button size="lg" variant="outline">
              WhatsApp
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="container flex flex-col gap-4 py-10 md:h-24 md:flex-row md:items-center md:justify-between md:py-0">
          <div className="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
            <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
              © 2025 Estúdio Madame. Todos os direitos reservados.
            </p>
          </div>
          <div className="flex items-center justify-center gap-4">
            <a className="text-sm text-muted-foreground hover:text-foreground" href="#">
              Instagram
            </a>
            <a className="text-sm text-muted-foreground hover:text-foreground" href="#">
              Facebook
            </a>
            <a className="text-sm text-muted-foreground hover:text-foreground" href="/dashboard">
              Dashboard
            </a>
            <a className="text-sm text-muted-foreground hover:text-foreground" href="#">
              Contato
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
