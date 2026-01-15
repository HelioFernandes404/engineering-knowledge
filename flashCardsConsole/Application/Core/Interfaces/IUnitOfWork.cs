using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Infrastructure.Persistence.Repositories;

namespace Application.Core.Interfaces
{
    public interface IUnitOfWork
    {
        ICardRepository CardRepo { get; }
        IDeckRepository DeckRepo { get; }
        void Commit();
    }
}
