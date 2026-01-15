using Application.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Core.Command;

namespace Application.Features.Decks.Commands
{
    public class ListDecksCommand : ICommand
    {
        private readonly DeckServices _deckServices;

        public ListDecksCommand(DeckServices deckServices)
        {
            _deckServices = deckServices ?? throw new ArgumentNullException(nameof(deckServices));
        }

        public async Task ExecuteAsync()
        {
            try
            {
                await _deckServices.ListarDecks();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao listar decks: {ex.Message}");
                throw;
            }
        }
    }
}
