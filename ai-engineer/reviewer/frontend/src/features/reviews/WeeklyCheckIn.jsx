import React, { useState, useEffect } from 'react';
import { cardApi } from '../../shared/api/cardApi';
import { Button } from '../../shared/ui/button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '../../shared/ui/card';
import { CheckCircle2, Circle, Calendar } from 'lucide-react';

const questions = [
  { id: 'q1', text: 'Implementei 3+ funções/modelos esta semana?' },
  { id: 'q2', text: 'Consegui refazer algo do D2 sem olhar?' },
  { id: 'q3', text: 'Projeto do sábado está funcional?' },
  { id: 'q4', text: 'Cards de revisão estão em dia?' },
  { id: 'q5', text: 'Estou em ritmo (20h/semana)?' },
];

export const WeeklyCheckIn = () => {
  const [answers, setAnswers] = useState({
    q1: false, q2: false, q3: false, q4: false, q5: false
  });
  const [completed, setCompleted] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await cardApi.getTodayCheckIn();
        if (response.data) {
          setCompleted(true);
        }
      } catch (error) {
        console.error('Error checking check-in status', error);
      } finally {
        setLoading(false);
      }
    };
    checkStatus();
  }, []);

  const toggleAnswer = (id) => {
    setAnswers(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const handleSubmit = async () => {
    try {
      await cardApi.submitCheckIn(answers);
      setCompleted(true);
    } catch (error) {
      console.error('Error submitting check-in', error);
    }
  };

  const isSunday = new Date().getDay() === 0;

  if (!isSunday && !completed) return null;
  if (loading) return null;
  
  if (completed) return (
    <Card className="bg-emerald-50/50 border-emerald-100 shadow-sm overflow-hidden">
      <div className="h-1 bg-emerald-500 w-full" />
      <CardContent className="py-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="bg-emerald-500 p-2 rounded-full">
            <CheckCircle2 className="h-5 w-5 text-white" />
          </div>
          <div>
            <p className="font-bold text-emerald-900">Reflexão Semanal Concluída</p>
            <p className="text-xs text-emerald-700/70 font-medium">Bom descanso, você merece este tempo offline.</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <Card className="border-indigo-100 shadow-xl shadow-indigo-50/50 overflow-hidden bg-white">
      <CardHeader className="bg-indigo-600 text-white pb-8">
        <div className="flex items-center gap-3 mb-2 opacity-80">
          <Calendar className="h-4 w-4" />
          <span className="text-xs font-bold uppercase tracking-widest">Ritual de Domingo</span>
        </div>
        <CardTitle className="text-2xl font-black">Check-in Semanal</CardTitle>
        <p className="text-indigo-100 text-sm mt-1 opacity-90">Reflita honestamente sobre sua jornada nos últimos 7 dias.</p>
      </CardHeader>
      
      <CardContent className="p-0">
        <div className="divide-y divide-slate-100">
          {questions.map((q) => (
            <div 
              key={q.id} 
              className={`flex items-center justify-between p-6 transition-all cursor-pointer group hover:bg-slate-50/80 ${answers[q.id] ? 'bg-indigo-50/30' : ''}`}
              onClick={() => toggleAnswer(q.id)}
            >
              <span className={`text-sm font-semibold transition-colors ${answers[q.id] ? 'text-indigo-900' : 'text-slate-600 group-hover:text-slate-900'}`}>
                {q.text}
              </span>
              <div className="relative">
                {answers[q.id] ? (
                  <CheckCircle2 className="h-7 w-7 text-indigo-600 animate-in zoom-in duration-300" />
                ) : (
                  <Circle className="h-7 w-7 text-slate-200 group-hover:text-slate-300 transition-colors" />
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
      
      <CardFooter className="p-6 bg-slate-50/50 border-t border-slate-100">
        <Button 
          className="w-full h-12 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-lg shadow-indigo-200 font-bold transition-all hover:-translate-y-0.5" 
          onClick={handleSubmit}
          disabled={!Object.values(answers).some(a => a)}
        >
          Finalizar Ritual e Descansar
        </Button>
      </CardFooter>
    </Card>
  );
};
