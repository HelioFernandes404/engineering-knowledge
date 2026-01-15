namespace FlashCardPlus.Domain.Models
{
    public class Deck
    {
        public int Id { get; set; }
        public string? Name { get; set; }

        public List<Card> Cards { get; set; } = new List<Card>();
    }
}