using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Domain.Entities
{
    public static class ConsoleManager
    {

        public static void PrintWithColor(string prefix, string text, ConsoleColor color)
        {
            var originalColor = Console.ForegroundColor;

            Console.ForegroundColor = color;

            Console.Write($"{prefix}{text}");

            Console.ForegroundColor = originalColor;

            Console.WriteLine();
        }
    }
}
