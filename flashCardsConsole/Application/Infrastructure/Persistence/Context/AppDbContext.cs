using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Domain.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace Application.Infrastructure.Persistence.Context
{
    public class AppDbContext(IConfiguration configuration) : DbContext
    {
        protected readonly IConfiguration Configuration = configuration;

        protected override void OnConfiguring(DbContextOptionsBuilder options)
        {
            // connect to sqlite database
            options.UseSqlite(Configuration.GetConnectionString("DatabaseLite"));
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Deck>()
                .HasMany(d => d.Cards)
                .WithOne(c => c.Deck)
                .HasForeignKey(c => c.DeckId);
        }

        public DbSet<Deck?> Decks { get; set; }
        public DbSet<Card> Cards { get; set; }
    }
}
