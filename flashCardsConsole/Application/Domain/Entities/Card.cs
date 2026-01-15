
namespace Application.Domain.Model
{
    public class Card
    {
        public int Id { get; set; }
        public string Question { get; set; }
        public string Answer { get; set; }
        public int Nivel { get; set; }
        public DateTime NextReviewDate { get; set; }


        // Chave estrangeira do Deck
        public int DeckId { get; set; }
        public Deck Deck { get; set; }

        public Card(string question, string answer)
        {
            Question = question;
            Answer = answer;
            Nivel = 0;
            NextReviewDate = DateTime.Now;
        }

        public Card()
        {
        }
    }
}
