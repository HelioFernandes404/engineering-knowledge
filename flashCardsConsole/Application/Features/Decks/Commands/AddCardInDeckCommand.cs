using Application.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Core.Command;

namespace Application.Features.Decks.Commands
{
    public class AddCardInDeckCommand : ICommand
    {
        private readonly DeckServices _deckServices;
        private readonly CardServices _cardServices;
        private readonly int _deckId;

        public AddCardInDeckCommand(DeckServices deckServices, CardServices cardServices, int deckId)
        {
            _deckServices = deckServices ?? throw new ArgumentNullException(nameof(deckServices));
            _deckId = deckId;
            _cardServices = cardServices ?? throw new ArgumentNullException(nameof(cardServices));
        }

        public async Task ExecuteAsync()
        {
            await _cardServices.AddCartas(_deckId);
        }
    }
}
