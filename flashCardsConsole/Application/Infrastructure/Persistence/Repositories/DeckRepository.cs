using Application.Domain.Model;
using Application.Infrastructure.Persistence.Context;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace Application.Infrastructure.Persistence.Repositories
{
    public interface IDeckRepository
    {
        Task<Deck> GetByIdAsync(int id);
        Task<IEnumerable<Deck>> GetAllAsync();
        Task CreateAsync(Deck deck);
        Task UpdateAsync(Deck deck);
        Task DeleteAsync(int id);
        Task<Deck> DeckIncludeCards(int id);
    }


    public class DeckRepository : IDeckRepository
    {

        private readonly AppDbContext _context;

        public DeckRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<Deck> GetByIdAsync(int id)
        {
            return await _context.Decks.FindAsync(id) 
                   ?? throw new InvalidOperationException
                       ($"Não foi possivel encontrar o deck com Id {id}");
        }

        public async Task<IEnumerable<Deck>> GetAllAsync()
        {
            return await _context.Decks.ToListAsync();
        }

        public Task CreateAsync(Deck deck)
        {
            throw new NotImplementedException();
        }

        public Task UpdateAsync(Deck deck)
        {
            throw new NotImplementedException();
        }

        public Task DeleteAsync(int id)
        {
            throw new NotImplementedException();
        }

        public async Task<Deck> DeckIncludeCards(int id)
        {
            return await _context.Decks.Include(d => d.Cards)
                .FirstOrDefaultAsync(d => d.Id == id);
        }
    }


}
