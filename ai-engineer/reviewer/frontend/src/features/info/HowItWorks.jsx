import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../shared/ui/card';
import { Button } from '../../shared/ui/button';
import { 
  BookOpen, 
  CheckCircle2, 
  Clock, 
  Zap, 
  ShieldAlert, 
  ArrowRight,
  Info
} from 'lucide-react';

export const HowItWorks = ({ onNavigate }) => {
  return (
    <div className="max-w-4xl mx-auto space-y-12 pb-20 animate-in fade-in duration-700">
      {/* Seção 1: O que é */}
      <section className="text-center space-y-4">
        <h2 className="text-3xl font-black text-slate-900 tracking-tight">O que é o Reviewer?</h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
          É o seu guia pessoal para transformar estudo passivo em <strong className="text-indigo-600">conhecimento real</strong>. 
          Focamos em ritmo e ritual, não em volume infinito.
        </p>
      </section>

      {/* Seção 2: Como usar no dia a dia */}
      <section className="space-y-6">
        <h3 className="text-xl font-bold text-slate-800 flex items-center gap-2 px-2">
          <Clock className="h-5 w-5 text-indigo-500" /> Seu Ritual Diário
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { step: '1', title: 'Abrir o "Hoje"', desc: 'Veja o que sua mente precisa revisar agora.' },
            { step: '2', title: 'Responder Cards', desc: 'Pratique a recuperação ativa da memória.' },
            { step: '3', title: 'Ajustar o Ritmo', desc: 'Siga as orientações para não sobrecarregar.' },
            { step: '4', title: 'Check-in Semanal', desc: 'Aos domingos, reflita sobre sua evolução.' },
          ].map((item) => (
            <Card key={item.step} className="border-0 shadow-sm bg-white ring-1 ring-slate-200/60 rounded-2xl">
              <CardContent className="p-6 flex gap-4">
                <span className="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-black text-sm">
                  {item.step}
                </span>
                <div className="space-y-1">
                  <h4 className="font-bold text-slate-900">{item.title}</h4>
                  <p className="text-sm text-slate-500 font-medium">{item.desc}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Seção 3: O que NÃO é */}
      <section className="p-8 rounded-[2rem] bg-slate-100/50 border border-slate-200/60 space-y-6">
        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
          <ShieldAlert className="h-5 w-5 text-slate-400" /> Alinhando Expectativas
        </h3>
        <ul className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <li className="space-y-2">
            <p className="font-bold text-sm text-slate-700">Não é um teste</p>
            <p className="text-xs text-slate-500 font-medium leading-relaxed">
              Errar faz parte. O Reviewer serve para identificar onde você precisa de mais prática.
            </p>
          </li>
          <li className="space-y-2">
            <p className="font-bold text-sm text-slate-700">Não é memória infinita</p>
            <p className="text-xs text-slate-500 font-medium leading-relaxed">
              Focamos no que é essencial para o seu plano mensal de estudo.
            </p>
          </li>
          <li className="space-y-2">
            <p className="font-bold text-sm text-slate-700">Não é só leitura</p>
            <p className="text-xs text-slate-500 font-medium leading-relaxed">
              Se você não está implementando o que aprende, o card não deve avançar.
            </p>
          </li>
        </ul>
      </section>

      {/* Seção 4: Quick Start */}
      <section className="bg-indigo-600 rounded-[2rem] p-10 text-white shadow-xl shadow-indigo-200 flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="space-y-4">
          <h3 className="text-2xl font-black">Pronto para começar?</h3>
          <ul className="space-y-2">
            <li className="flex items-center gap-2 text-indigo-100 text-sm font-bold">
              <CheckCircle2 className="h-4 w-4" /> Cadastre o seu primeiro Mês
            </li>
            <li className="flex items-center gap-2 text-indigo-100 text-sm font-bold">
              <CheckCircle2 className="h-4 w-4" /> Adicione 3 tópicos essenciais
            </li>
          </ul>
        </div>
        <div className="flex flex-col sm:flex-row gap-4">
          <Button 
            className="bg-white text-indigo-600 hover:bg-indigo-50 font-bold px-8 rounded-xl h-12"
            onClick={() => onNavigate('plan')}
          >
            Configurar Mês <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
          <Button 
            variant="ghost" 
            className="text-white hover:bg-indigo-500 font-bold px-8 rounded-xl h-12 border border-indigo-400"
            onClick={() => onNavigate('today')}
          >
            Ir para Hoje
          </Button>
        </div>
      </section>

      {/* Seção 5: Por que funciona */}
      <section className="text-center space-y-8 pt-4">
        <h3 className="text-sm font-black uppercase tracking-[0.2em] text-slate-400">A Ciência por trás</h3>
        <div className="flex flex-wrap justify-center gap-10">
          <div className="max-w-[200px] space-y-2">
            <Zap className="h-6 w-6 text-amber-500 mx-auto" />
            <p className="font-bold text-sm text-slate-800 uppercase tracking-tight">Recuperação Ativa</p>
            <p className="text-xs text-slate-500 font-medium">Forçar a mente a lembrar fortalece as conexões neurais.</p>
          </div>
          <div className="max-w-[200px] space-y-2">
            <Clock className="h-6 w-6 text-blue-500 mx-auto" />
            <p className="font-bold text-sm text-slate-800 uppercase tracking-tight">Efeito de Espaçamento</p>
            <p className="text-xs text-slate-500 font-medium">Revisar no momento certo evita a curva do esquecimento.</p>
          </div>
          <div className="max-w-[200px] space-y-2">
            <BookOpen className="h-6 w-6 text-emerald-500 mx-auto" />
            <p className="font-bold text-sm text-slate-800 uppercase tracking-tight">Aplicação Direta</p>
            <p className="text-xs text-slate-500 font-medium">Implementar antes de ler garante que o conhecimento é prático.</p>
          </div>
        </div>
      </section>
    </div>
  );
};
