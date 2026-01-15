using Application.Domain.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Domain.Entities
{
    public static class DeckManager
    {


        public static void PrintDeckList(List<Deck> decks)
        {
            foreach (var deck in decks)
            {
                Console.WriteLine($"Id: {deck.Id}  || Deck:{deck.Name}");
            }
        }

    }
}
