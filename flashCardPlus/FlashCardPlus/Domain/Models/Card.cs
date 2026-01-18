namespace FlashCardPlus.Domain.Models
{
    public class Card
    {
        public int Id { get; set; }
        public string Front { get; set; } = string.Empty;
        public string Back { get; set; }
    }
}