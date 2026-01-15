using System.Linq.Expressions;
using EFcore.Domain;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace DominandoEFCore;

public class ConversorCustomizado : ValueConverter<Status, string>
{
    public ConversorCustomizado() : base
    (
        db => ConverterParaOhBancoDeDados(db),
        value => ConverterParaAplicacao(value),
        new ConverterMappingHints(size: 1)
    )
    { }

    static string ConverterParaOhBancoDeDados(Status status)
    {
        return status.ToString()[0..1];
    }
    static Status ConverterParaAplicacao(string value)
    {
        var status = Enum.GetValues<Status>()
            .FirstOrDefault(p => p.ToString()[0..1] == value); // pega o primeiro valor que corresponde ao valor passado

        return status;
    }
}

