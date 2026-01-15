using Microsoft.EntityFrameworkCore;
using Application.Domain.Model;
using Application.Infrastructure.Persistence.Context;

namespace Application.Services
{
    public class CardServices
    {
        private readonly AppDbContext _context;

        public CardServices(AppDbContext context)
        {
            _context = context;
        }

        public async Task AddCartas(int deckId)
        {
            var deck = await _context.Decks
                .Include(d => d.Cards)
                .FirstOrDefaultAsync(d => d.Id == deckId);

            if (deck == null)
            {
                Console.WriteLine("Deck não encontrado.");
                return;
            }

            Console.WriteLine("Por favor, insira o caminho completo do arquivo CSV:");
            string filePath = Console.ReadLine();

            if (File.Exists(filePath))
            {
                var lines = File.ReadAllLines(filePath);

                foreach (var line in lines)
                {
                    var data = line.Split(',');

                    if (data.Length >= 2) // Exemplo: pergunta e resposta
                    {
                        var card = new Card
                        {
                            Question = data[0], // Pergunta da carta
                            Answer = data[1],   // Resposta da carta
                            DeckId = deckId
                        };

                        deck.Cards.Add(card);
                    }
                }

                await _context.SaveChangesAsync();
                Console.WriteLine("Cartas adicionadas com sucesso.");
            }
            else
            {
                Console.WriteLine("Arquivo não encontrado. Verifique o caminho e tente novamente.");
            }
        }

    }
}
