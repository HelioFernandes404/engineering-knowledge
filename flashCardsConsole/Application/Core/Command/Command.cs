using Application.Services;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Core.Command
{
    public interface ICommand
    {
        Task ExecuteAsync();
    }

    public class CommandInvoker
    {
        private readonly Dictionary<string, Func<IServiceScope, ICommand>> _commandFactories;
        private readonly IServiceProvider _serviceProvider;

        public CommandInvoker(IServiceProvider serviceProvider)
        {
            _serviceProvider = serviceProvider;
            _commandFactories = new Dictionary<string, Func<IServiceScope, ICommand>>();
        }

        public void RegisterCommand(string name, Func<IServiceScope, ICommand> factory)
        {
            _commandFactories[name] = factory;
        }

        public async Task ExecuteCommandAsync(string name)
        {
            if (_commandFactories.ContainsKey(name))
            {
                using (var scope = _serviceProvider.CreateScope())
                {
                    var command = _commandFactories[name](scope);
                    await command.ExecuteAsync();
                }
            }
        }
    }
}
