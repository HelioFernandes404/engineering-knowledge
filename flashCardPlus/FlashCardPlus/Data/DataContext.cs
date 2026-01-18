using FlashCardPlus.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace FlashCardPlus.Data
{
    public class DataContext : DbContext
    {
        protected readonly IConfiguration Configuration;

        public DataContext(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder options)
        {
            options.UseSqlite(Configuration.GetConnectionString("DatabaseLite"));
        }

        public DbSet<Deck> Decks { get; set; }
        public DbSet<Card> Cards { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Deck>().HasData(
                new Deck { Id = 1, Name = "Frases Básicas" },
                new Deck { Id = 2, Name = "Frases Intermediárias" }
            );

            modelBuilder.Entity<Card>().HasData(
                new Card { Id = 1, Front = "Hello, how are you?", Back = "Olá, como você está?" },
                new Card { Id = 2, Front = "I am learning English.", Back = "Eu estou aprendendo inglês." },
                new Card { Id = 3, Front = "What is your name?", Back = "Qual é o seu nome?" }
            );

        }
    }
}