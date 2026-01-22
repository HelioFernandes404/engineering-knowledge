import React, { useState, useEffect } from 'react';
import { cardApi } from '@/shared/api/cardApi';
import { Button } from '@/shared/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/ui/card';
import { Check, X, Info } from 'lucide-react';
import { WeeklyCheckIn } from './WeeklyCheckIn';
import { PaceRecommendations } from './PaceRecommendations';

export function TodayReviews({ onReviewComplete }) {

  const [pendingCards, setPendingCards] = useState([]);

  const [currentIndex, setCurrentIndex] = useState(0);

  const [showPace, setShowPace] = useState(false);



  const fetchToday = async () => {

    try {

      const response = await cardApi.getTodayCards();

      setPendingCards(response.data);

      setCurrentIndex(0);

    } catch (error) {

      console.error('Failed to fetch today cards', error);

    }

  };



  useEffect(() => {

    fetchToday();

  }, []);



  const handleReview = async (success) => {

    const card = pendingCards[currentIndex];

    try {

      await cardApi.reviewCard(card.id, success);

      if (currentIndex + 1 < pendingCards.length) {

        setCurrentIndex(currentIndex + 1);

      } else {

        setPendingCards([]);

        if (onReviewComplete) onReviewComplete();

      }

    } catch (error) {

      console.error('Failed to review card', error);

    }

  };



  const progress = pendingCards.length > 0 

    ? ((currentIndex) / pendingCards.length) * 100 

    : 100;



  return (

    <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">

      <div className="lg:col-span-8 space-y-8">

        <WeeklyCheckIn />

        

        {pendingCards.length > 0 ? (

          <div className="space-y-6">

            <div className="flex items-center justify-between px-2">

              <div className="space-y-1">

                <h2 className="text-xl font-bold text-slate-800">Sessão de Revisão</h2>

                <p className="text-sm text-slate-500 font-medium">Card {currentIndex + 1} de {pendingCards.length}</p>

              </div>

              <div className="text-right">

                <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1.5 rounded-full border border-indigo-100">

                  {Math.round(progress)}% Concluído

                </span>

              </div>

            </div>



            <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">

              <div 

                className="bg-indigo-600 h-full transition-all duration-500 ease-out shadow-[0_0_8px_rgba(79,70,229,0.4)]"

                style={{ width: `${progress}%` }}

              />

            </div>



            <Card className="shadow-2xl shadow-indigo-100/50 border-0 bg-white overflow-hidden ring-1 ring-slate-200/60">

              <div className="h-2 bg-indigo-600 w-full" />

              <CardContent className="p-0">

                <div className="min-h-[300px] flex items-center justify-center p-12 text-center">

                  <h3 className="text-3xl md:text-4xl font-semibold text-slate-800 leading-tight tracking-tight">

                    {pendingCards[currentIndex].question}

                  </h3>

                </div>

                

                <div className="grid grid-cols-2 border-t border-slate-100">

                  <button 

                    className="flex flex-col items-center justify-center py-8 gap-2 bg-white hover:bg-red-50 text-slate-400 hover:text-red-600 transition-all duration-200 group border-r border-slate-100"

                    onClick={() => handleReview(false)}

                  >

                    <div className="bg-slate-100 group-hover:bg-red-100 p-3 rounded-full transition-colors">

                      <X className="h-6 w-6" />

                    </div>

                    <span className="text-xs font-bold uppercase tracking-widest">Reiniciar (D2)</span>

                  </button>

                  <button 

                    className="flex flex-col items-center justify-center py-8 gap-2 bg-white hover:bg-emerald-50 text-slate-400 hover:text-emerald-600 transition-all duration-200 group"

                    onClick={() => handleReview(true)}

                  >

                    <div className="bg-slate-100 group-hover:bg-emerald-100 p-3 rounded-full transition-colors">

                      <Check className="h-6 w-6" />

                    </div>

                    <span className="text-xs font-bold uppercase tracking-widest">Avançar</span>

                  </button>

                </div>

              </CardContent>

            </Card>

            

            <p className="text-center text-slate-400 text-xs font-medium italic italic">

              Dica: Foque no "porquê" antes de avançar.

            </p>

          </div>

        ) : (

          <Card className="border-0 shadow-xl shadow-slate-200/50 bg-white overflow-hidden">

            <div className="h-1.5 bg-emerald-500 w-full" />

            <CardContent className="p-16 text-center space-y-6">

              <div className="inline-flex items-center justify-center w-20 h-20 bg-emerald-50 rounded-full mb-2">

                <Check className="h-10 w-10 text-emerald-500" />

              </div>

              <div className="space-y-2">

                <h3 className="text-2xl font-black text-slate-900">Ritual Concluído!</h3>

                <p className="text-slate-500 max-w-xs mx-auto">Sua mente está afiada. Todos os tópicos de hoje foram revisados com sucesso.</p>

              </div>

              <Button 

                variant="outline" 

                className="rounded-xl border-slate-200 text-slate-600 hover:bg-slate-50 font-semibold px-8" 

                onClick={fetchToday}

              >

                Recarregar cards

              </Button>

            </CardContent>

          </Card>

        )}

      </div>



      <aside className="lg:col-span-4 space-y-6 lg:sticky lg:top-8">

        <div className="p-6 bg-white rounded-3xl border border-slate-200/60 shadow-sm space-y-4">

          <div className="flex items-center gap-3 mb-2">

            <div className="p-2 bg-amber-50 rounded-lg">

              <Info className="h-5 w-5 text-amber-600" />

            </div>

            <h4 className="font-bold text-slate-800">Seu Ritmo</h4>

          </div>

          

          <PaceRecommendations pendingCount={pendingCards.length} />

          

          {!showPace && pendingCards.length === 0 && (

             <Button 

                variant="ghost" 

                className="w-full text-xs font-bold text-slate-400 hover:text-slate-600 uppercase tracking-widest"

                onClick={() => setShowPace(true)}

             >

               Ver recomendações completas

             </Button>

          )}

        </div>

      </aside>

    </div>

  );

}
