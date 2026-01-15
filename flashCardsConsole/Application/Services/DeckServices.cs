using Application.Core.Interfaces;
using Application.Domain.Entities;
using Application.Domain.Model;
using Application.Infrastructure.Persistence.Context;
using Application.Infrastructure.Services.TTSService;
using Microsoft.EntityFrameworkCore;

namespace Application.Services
{
    public class DeckServices(TTSService ttsService, IUnitOfWork repoUow, AppDbContext context)
    {
        private IUnitOfWork _repoUow = repoUow;
        private AppDbContext _context = context;

        public async Task ListarDecks()
        {
            Console.WriteLine("\nPara começar estudar um deck digite: start /{DeckId}");
            var listAsync = await _repoUow.DeckRepo.GetAllAsync();
            DeckManager.PrintDeckList(listAsync.ToList());
        }

        public async Task<Deck> ExibirCartasDoBaralho(int deckId)
        {
            var decksResult = await _repoUow.DeckRepo.DeckIncludeCards(deckId);

            if (decksResult == null)
            {
                Console.WriteLine("Deck não encontrado.");
                return null;
            }

            foreach (var card in decksResult.Cards)
            {
                if (card.NextReviewDate <= DateTime.Now)
                {
                    Console.WriteLine("\nConvertTextToSpeechAndPlay Aguarde...");
                    await ttsService.ConvertTextToSpeechAndPlay(card.Question);
                    Console.WriteLine("\nPressione qualquer tecla para: virar a carta");
                    Console.ReadKey(intercept: true);

                    PrintWithColor($"Frente: ", card.Question, ConsoleColor.Red);
                    Console.WriteLine("Pressione qualquer tecla para ver o verso...");
          

                    var key = Console.ReadKey(intercept: true);
                    if (key.KeyChar == 'z')
                    {
                        Console.WriteLine("Repetindo a frase...");
                        await ttsService.ConvertTextToSpeechAndPlay(card.Question);
                        Console.ReadKey();
                    }

                    PrintWithColor($"Verso: ", card.Answer, ConsoleColor.Red);
                    Console.WriteLine("\nAvalie sua resposta:");

                    PrintWithColor("q: ", "Repetir ", ConsoleColor.DarkRed);
                    PrintWithColor("w: ", "Fácil   (revisar em 1 dia)", ConsoleColor.Yellow);
                    PrintWithColor("e: ", "Muito Fácil (revisar em 2 dias)", ConsoleColor.Blue);
                    PrintWithColor("r: ", "Fluente (revisar em 3 dias)", ConsoleColor.Green);

                    var response = Console.ReadKey(intercept: true);
                    switch (response.KeyChar)
                    {
                        case 'q':
                            card.NextReviewDate = DateTime.Now;
                            break;
                        case 'w':
                            card.NextReviewDate = DateTime.Now.AddDays(1);
                            break;
                        case 'e':
                            card.NextReviewDate = DateTime.Now.AddDays(2);
                            break;
                        case 'r':
                            card.NextReviewDate = DateTime.Now.AddDays(3);
                            break;
                        default:
                            Console.WriteLine("Resposta inválida. Tente novamente.");
                            card.NextReviewDate = DateTime.Now;
                            break;
                    }

                    await _context.SaveChangesAsync();
                    Console.Clear();
                }
            }

            return decksResult;
        }

        static void PrintWithColor(string prefix, string text, ConsoleColor color)
        {
            var originalColor = Console.ForegroundColor;

            Console.ForegroundColor = color;

            Console.Write($"{prefix}{text}");

            Console.ForegroundColor = originalColor;

            Console.WriteLine();
        }

    }
}