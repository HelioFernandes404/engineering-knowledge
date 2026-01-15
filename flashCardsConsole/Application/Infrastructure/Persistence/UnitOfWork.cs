using Application.Core.Interfaces;
using Application.Infrastructure.Persistence.Context;
using Application.Infrastructure.Persistence.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Infrastructure.Persistence
{
    public class UnitOfWork : IUnitOfWork
    {
        public ICardRepository _cardRepository;
        public IDeckRepository _deckRepository;
        public AppDbContext _context;

        public UnitOfWork(AppDbContext context)
        {
            _context = context;
        }

        public ICardRepository CardRepo
        {
            get
            {
                if (_cardRepository == null)
                {
                    _cardRepository = new CardRepository(_context);
                }
                return _cardRepository;
            }
        }

        public IDeckRepository DeckRepo
        {
            get
            {
                if (_deckRepository == null)
                {
                    _deckRepository = new DeckRepository(_context);
                }
                return _deckRepository;
            }
        }


        public void Commit()
        {
            _context.SaveChanges();
        }
    }

}
