import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../shared/ui/card';
import { Rocket, Gauge, BookOpen } from 'lucide-react';

export const PaceRecommendations = ({ pendingCount }) => {
  return (
    <div className="space-y-4">
      {pendingCount < 5 && (
        <div className="p-4 rounded-2xl bg-orange-50/50 border border-orange-100 space-y-3 animate-in slide-in-from-right-4 duration-300">
          <div className="flex items-center gap-2 text-orange-700">
            <Rocket className="h-4 w-4" />
            <span className="text-xs font-bold uppercase tracking-wider">Acelerar Ritmo</span>
          </div>
          <div className="space-y-2">
            <p className="text-[11px] font-bold text-orange-800/80 leading-relaxed uppercase">
              Se as revisões estão rápidas demais:
            </p>
            <ul className="text-xs text-orange-700/80 space-y-1.5 font-medium">
              <li className="flex items-center gap-2">
                <div className="h-1 w-1 rounded-full bg-orange-300" />
                Aprofunde com papers e variações
              </li>
              <li className="flex items-center gap-2">
                <div className="h-1 w-1 rounded-full bg-orange-300" />
                Contribua para projetos open source
              </li>
              <li className="flex items-center gap-2">
                <div className="h-1 w-1 rounded-full bg-orange-300" />
                Inicie uma especialização paralela
              </li>
            </ul>
          </div>
        </div>
      )}

      {pendingCount > 15 && (
        <div className="p-4 rounded-2xl bg-indigo-50/50 border border-indigo-100 space-y-3 animate-in slide-in-from-right-4 duration-300">
          <div className="flex items-center gap-2 text-indigo-700">
            <Gauge className="h-4 w-4" />
            <span className="text-xs font-bold uppercase tracking-wider">Ajustar Foco</span>
          </div>
          <div className="space-y-2">
            <p className="text-[11px] font-bold text-indigo-800/80 leading-relaxed uppercase">
              Se as revisões estão acumulando:
            </p>
            <ul className="text-xs text-indigo-700/80 space-y-1.5 font-medium">
              <li className="flex items-center gap-2">
                <div className="h-1 w-1 rounded-full bg-indigo-300" />
                Reduza projetos secundários
              </li>
              <li className="flex items-center gap-2">
                <div className="h-1 w-1 rounded-full bg-indigo-300" />
                Pause tópicos opcionais do mês
              </li>
              <li className="flex items-center gap-2">
                <div className="h-1 w-1 rounded-full bg-indigo-300" />
                Ajuste sua carga horária semanal
              </li>
            </ul>
          </div>
        </div>
      )}

      <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-3">
        <div className="flex items-center gap-2 text-slate-600">
          <BookOpen className="h-4 w-4" />
          <span className="text-xs font-bold uppercase tracking-wider">Cognição</span>
        </div>
        <div className="space-y-2">
          <p className="text-[11px] font-bold text-slate-500 leading-relaxed uppercase">
            Dificuldade com a leitura?
          </p>
          <ul className="text-xs text-slate-600/80 space-y-1.5 font-medium">
            <li className="flex items-center gap-2">
              <div className="h-1 w-1 rounded-full bg-slate-300" />
              Use ferramentas de Text-to-Speech
            </li>
            <li className="flex items-center gap-2">
              <div className="h-1 w-1 rounded-full bg-slate-300" />
              Priorize demonstrações em vídeo
            </li>
            <li className="flex items-center gap-2">
              <div className="h-1 w-1 rounded-full bg-slate-300" />
              Codifique antes de ler a teoria
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
