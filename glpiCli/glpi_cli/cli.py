# -*- coding: utf-8 -*-
"""GLPI CLI - Command-line interface for GLPI REST API."""
import click
import sys
from .config import Config
from .client import GLPIClient
from .errors import GLPIError
from .utils import normalize_itemtype, get_available_itemtypes
from .formatters import (
    format_json,
    format_table,
    format_single_item,
    print_error,
    print_success,
    print_info,
)


def get_client() -> GLPIClient:
    """Initialize and validate GLPI client.

    Returns:
        Configured GLPIClient instance

    Raises:
        GLPIError: If configuration is invalid
    """
    config = Config()
    is_valid, error_msg = config.validate()

    if not is_valid:
        print_error(f"Configura��o inv�lida: {error_msg}")
        print_info("Configure as vari�veis de ambiente ou crie ~/.config/glpi/config.yml")
        sys.exit(1)

    return GLPIClient(config)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """GLPI CLI - Ferramenta de debug para GLPI REST API.

    \b
    Exemplos:
      glpi list ticket
      glpi get computer 42
      glpi search entity
      glpi info
    """
    pass


@cli.command()
@click.argument("itemtype")
@click.option("--limit", default=50, help="N�mero m�ximo de itens (padr�o: 50)")
@click.option("--start", default=0, help="�ndice inicial para pagina��o (padr�o: 0)")
@click.option("--json", "as_json", is_flag=True, help="Sa�da em formato JSON")
def list(itemtype: str, limit: int, start: int, as_json: bool):
    """Listar items de um tipo espec�fico.

    \b
    Exemplos:
      glpi list ticket
      glpi list computer --limit 100
      glpi list entity --json
    """
    itemtype = normalize_itemtype(itemtype)
    client = get_client()

    try:
        client.init_session()
        items = client.list_items(itemtype, range_start=start, range_limit=limit)

        if as_json:
            click.echo(format_json(items))
        else:
            format_table(items)

    except GLPIError as e:
        print_error(str(e))
        sys.exit(1)
    finally:
        client.kill_session()


@cli.command()
@click.argument("itemtype")
@click.argument("item_id", type=int)
@click.option("--json", "as_json", is_flag=True, help="Sa�da em formato JSON")
def get(itemtype: str, item_id: int, as_json: bool):
    """Obter um item espec�fico por ID.

    \b
    Exemplos:
      glpi get ticket 123
      glpi get computer 42
      glpi get entity 5 --json
    """
    itemtype = normalize_itemtype(itemtype)
    client = get_client()

    try:
        client.init_session()
        item = client.get_item(itemtype, item_id)

        if as_json:
            click.echo(format_json(item))
        else:
            format_single_item(item)

    except GLPIError as e:
        print_error(str(e))
        sys.exit(1)
    finally:
        client.kill_session()


@cli.command()
@click.argument("itemtype")
@click.option("--field", default=1, help="Campo para busca (padr�o: 1 = name)")
@click.option("--value", required=True, help="Valor a buscar")
@click.option("--searchtype", default="contains", help="Tipo de busca (padr�o: contains)")
@click.option("--json", "as_json", is_flag=True, help="Sa�da em formato JSON")
def search(itemtype: str, field: int, value: str, searchtype: str, as_json: bool):
    """Buscar items com crit�rios.

    \b
    Exemplos:
      glpi search ticket --value "servidor"
      glpi search computer --field 1 --value "srv-web"
      glpi search entity --value "TI" --json
    """
    itemtype = normalize_itemtype(itemtype)
    client = get_client()

    criteria = [{"field": field, "searchtype": searchtype, "value": value}]

    try:
        client.init_session()
        items = client.search_items(itemtype, criteria=criteria)

        if as_json:
            click.echo(format_json(items))
        else:
            format_table(items)

    except GLPIError as e:
        print_error(str(e))
        sys.exit(1)
    finally:
        client.kill_session()


@cli.command()
@click.argument("itemtype")
@click.argument("item_id", type=int)
@click.option("--json", "as_json", is_flag=True, help="Saída em formato JSON")
def fingerprint(itemtype: str, item_id: int, as_json: bool):
    """Obter dados de fingerprint (Plugin Fields) para um item específico.

    \b
    Exemplos:
      glpi fingerprint problem 123
      glpi fingerprint ticket 42 --json
    """
    itemtype = normalize_itemtype(itemtype)
    client = get_client()

    try:
        client.init_session()
        data = client.get_fingerprint(itemtype, item_id)

        if as_json:
            click.echo(format_json(data))
        else:
            format_single_item(data)

    except GLPIError as e:
        print_error(str(e))
        sys.exit(1)
    finally:
        client.kill_session()


@cli.command()
@click.argument("itemtype")
@click.option("--limit", default=50, help="Número máximo de itens (padrão: 50)")
@click.option("--start", default=0, help="Índice inicial para paginação (padrão: 0)")
@click.option("--json", "as_json", is_flag=True, help="Saída em formato JSON")
def fingerprints(itemtype: str, limit: int, start: int, as_json: bool):
    """Listar todos os dados de fingerprint (Plugin Fields) de um tipo de item.

    \b
    Exemplos:
      glpi fingerprints problem
      glpi fingerprints ticket --limit 100 --json
    """
    itemtype = normalize_itemtype(itemtype)
    client = get_client()

    try:
        client.init_session()
        items = client.list_fingerprints(itemtype, range_start=start, range_limit=limit)

        if as_json:
            click.echo(format_json(items))
        else:
            format_table(items)

    except GLPIError as e:
        print_error(str(e))
        sys.exit(1)
    finally:
        client.kill_session()


@cli.command()
@click.argument("itemtype")
@click.option("--value", required=True, help="Valor do fingerprint a buscar")
@click.option("--json", "as_json", is_flag=True, help="Saída em formato JSON")
def fingerprint_search(itemtype: str, value: str, as_json: bool):
    """Buscar items por valor de fingerprint (Plugin Fields).

    \b
    Exemplos:
      glpi fingerprint-search problem --value "abc123xyz"
      glpi fingerprint-search ticket --value "hash-value" --json
    """
    itemtype = normalize_itemtype(itemtype)
    client = get_client()

    try:
        client.init_session()
        items = client.search_fingerprint(itemtype, value)

        if as_json:
            click.echo(format_json(items))
        else:
            format_table(items)

    except GLPIError as e:
        print_error(str(e))
        sys.exit(1)
    finally:
        client.kill_session()


@cli.command()
def info():
    """Mostrar informa��es de configura��o e ItemTypes dispon�veis."""
    config = Config()
    is_valid, error_msg = config.validate()

    print_info("Configura��o GLPI CLI")
    click.echo(f"\nURL: {config.url}")
    click.echo(f"App Token: {' configurado' if config.app_token else ' n�o configurado'}")
    click.echo(f"User Token: {' configurado' if config.user_token else ' n�o configurado'}")

    if not is_valid:
        print_error(f"\nErro: {error_msg}")
        sys.exit(1)
    else:
        print_success("\nConfigura��o v�lida!")

    click.echo("\n" + "=" * 50)
    click.echo("ItemTypes comuns dispon�veis:")
    click.echo("=" * 50)

    itemtypes = get_available_itemtypes()
    for i, itemtype in enumerate(itemtypes, 1):
        click.echo(f"  {i:2}. {itemtype}")

    click.echo(f"\nTotal: {len(itemtypes)} itemtypes")


def main():
    """Entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()
