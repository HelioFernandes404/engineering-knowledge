using Application.Domain.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Core.Interfaces;
using Application.Infrastructure.Persistence.Context;

namespace Application.Infrastructure.Persistence.Repositories
{
    public interface ICardRepository
    {
        Task<Card> GetByIdAsync(int id);
        Task<IEnumerable<Card>> GetAllAsync();
        Task AddAsync(Card card);
        Task UpdateAsync(Card card);
        Task DeleteAsync(int id);
    }


    public class CardRepository : ICardRepository
    {
        private readonly AppDbContext _context;

        public CardRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<Card> GetByIdAsync(int id)
        {
            return await _context.Cards.FindAsync(id);
        }

        public Task<IEnumerable<Card>> GetAllAsync()
        {
            throw new NotImplementedException();
        }

        public Task AddAsync(Card card)
        {
            throw new NotImplementedException();
        }

        public Task UpdateAsync(Card card)
        {
            throw new NotImplementedException();
        }

        public Task DeleteAsync(int id)
        {
            throw new NotImplementedException();
        }

        // Implementação dos outros métodos...
    }
}
