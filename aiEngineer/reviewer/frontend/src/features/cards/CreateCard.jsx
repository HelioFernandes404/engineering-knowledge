import React, { useState, useEffect } from 'react';
import { cardApi } from '@/shared/api/cardApi';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/ui/card';

export function CreateCard({ onCardCreated }) {
  const [question, setQuestion] = useState('');
  const [monthId, setMonthId] = useState('');
  const [initialStage, setInitialStage] = useState(0);
  const [months, setMonths] = useState([]);

  useEffect(() => {
    const fetchMonths = async () => {
      try {
        const response = await cardApi.getMonths();
        setMonths(response.data);
        if (response.data.length > 0) {
          setMonthId(response.data[0].id);
        }
      } catch (error) {
        console.error('Failed to fetch months', error);
      }
    };
    fetchMonths();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    try {
      await cardApi.createCard({
        question,
        month_id: monthId ? parseInt(monthId) : null,
        current_stage: parseInt(initialStage)
      });
      setQuestion('');
      if (onCardCreated) onCardCreated();
    } catch (error) {
      console.error('Failed to create card', error);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto mt-8 border-l-4 border-l-blue-600">
      <CardHeader>
        <CardTitle>Adicionar ao Plano de Estudo</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase">Pergunta</label>
            <Input
              id="question"
              name="question"
              placeholder="Ex: Qual a complexidade do QuickSort?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">Mês</label>
              <select 
                className="w-full h-10 px-3 py-2 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={monthId}
                onChange={(e) => setMonthId(e.target.value)}
              >
                {months.map(m => (
                  <option key={m.id} value={m.id}>{m.title}</option>
                ))}
                {months.length === 0 && <option value="">Nenhum mês</option>}
              </select>
            </div>
            
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase">Estágio Inicial</label>
              <select 
                className="w-full h-10 px-3 py-2 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={initialStage}
                onChange={(e) => setInitialStage(e.target.value)}
              >
                <option value="0">D0 (Novo)</option>
                <option value="1">D2</option>
                <option value="2">D7</option>
                <option value="3">D14</option>
                <option value="4">D30</option>
              </select>
            </div>
          </div>
          
          <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">Adicionar ao Plano</Button>
        </form>
      </CardContent>
    </Card>
  );
}