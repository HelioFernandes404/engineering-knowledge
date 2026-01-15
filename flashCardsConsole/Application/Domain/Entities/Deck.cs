using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Domain.Model
{
    public class Deck
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public ICollection<Card> Cards { get; set; }
    }
}
