import React from 'react';
import { cardApi } from '@/shared/api/cardApi';
import { Button } from '@/shared/ui/button';
import { Card, CardContent } from '@/shared/ui/card';
import { Trash2 } from 'lucide-react';

export function CardList({ cards, onCardDeleted }) {
  const handleDelete = async (id) => {
    try {
      await cardApi.deleteCard(id);
      if (onCardDeleted) onCardDeleted();
    } catch (error) {
      console.error('Failed to delete card', error);
    }
  };

  return (
    <div className="space-y-4 mt-8">
      <h2 className="text-xl font-bold">Todos os Cards ({cards.length})</h2>
      {cards.map((card) => (
        <Card key={card.id}>
          <CardContent className="p-4 flex justify-between items-center">
            <div>
              <p className="font-medium">{card.question}</p>
              <p className="text-sm text-gray-500">Estágio: {card.current_stage} | Próxima: {card.next_review_date}</p>
            </div>
            <Button variant="ghost" size="icon" onClick={() => handleDelete(card.id)}>
              <Trash2 className="h-4 w-4 text-red-500" />
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
