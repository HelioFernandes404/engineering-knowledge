"""Interactive CLI for LinkedIn Query Helper."""

import webbrowser
import questionary
from questionary import Style
from .url_builder import build_job_search_url, build_content_search_url
from .constants import (
    WORKPLACE_TYPE_OPTIONS,
    DATE_POSTED_OPTIONS,
    EXPERIENCE_LEVEL_OPTIONS,
    JOB_TYPE_OPTIONS,
    TECH_SUGGESTIONS,
)

# Custom style matching LinkedIn colors
custom_style = Style(
    [
        ("qmark", "fg:#0a66c2 bold"),
        ("question", "bold"),
        ("answer", "fg:#0a66c2 bold"),
        ("pointer", "fg:#0a66c2 bold"),
        ("highlighted", "fg:#0a66c2 bold"),
        ("selected", "fg:#0a66c2"),
        ("separator", "fg:#6c6c6c"),
        ("instruction", "fg:#6c6c6c"),
    ]
)


def get_exclude_keywords() -> list:
    """Get excluded keywords from user."""
    exclude_input = questionary.text(
        "Excluir palavras-chave (separadas por vírgula, opcional):", style=custom_style
    ).ask()

    if not exclude_input:
        return []

    return [k.strip() for k in exclude_input.split(",") if k.strip()]


def get_page_number() -> int:
    """Get page number from user."""
    while True:
        page = questionary.text(
            "Página de pesquisa:", default="1", style=custom_style
        ).ask()

        try:
            page_num = int(page)
            if page_num < 1:
                print("❌ Página deve ser maior que 0")
                continue
            return page_num
        except ValueError:
            print("❌ Digite um número válido")


def collect_job_search_data():
    """Collect job search parameters from user."""
    print("\n🔎 LinkedIn Query Helper - Busca de Vagas\n")

    # Technology
    tech = questionary.autocomplete(
        "Tecnologia/palavra-chave:", choices=TECH_SUGGESTIONS, style=custom_style
    ).ask()

    if not tech:
        return None

    # Exclude keywords
    exclude = get_exclude_keywords()

    # Workplace type (multiple selection)
    workplace_choices = [
        questionary.Choice(label, value=value)
        for value, label in WORKPLACE_TYPE_OPTIONS.items()
    ]
    workplace_type = questionary.checkbox(
        "Modalidade de trabalho (use espaço para selecionar):",
        choices=workplace_choices,
        style=custom_style,
    ).ask()

    if workplace_type is None:
        return None

    # Experience Level (Senioridade) - multiple selection
    experience_choices = [
        questionary.Choice(label, value=value)
        for value, label in EXPERIENCE_LEVEL_OPTIONS.items()
    ]
    experience_level = questionary.checkbox(
        "Nível de senioridade (use espaço para selecionar):",
        choices=experience_choices,
        style=custom_style,
    ).ask()

    if experience_level is None:
        return None

    # Job Type (Tipo de Contrato) - multiple selection
    job_type_choices = [
        questionary.Choice(label, value=value)
        for value, label in JOB_TYPE_OPTIONS.items()
    ]
    job_type = questionary.checkbox(
        "Tipo de contrato (use espaço para selecionar):",
        choices=job_type_choices,
        style=custom_style,
    ).ask()

    if job_type is None:
        return None

    # Date posted
    date_choices = [
        questionary.Choice(label, value=value)
        for value, label in DATE_POSTED_OPTIONS.items()
    ]
    date_posted = questionary.select(
        "Publicada há:", choices=date_choices, default="any", style=custom_style
    ).ask()

    if not date_posted:
        return None

    # Easy Apply
    easy_apply = questionary.confirm(
        "Apenas Easy Apply?", default=False, style=custom_style
    ).ask()

    if easy_apply is None:
        return None

    # Jobs In Your Network
    in_your_network = questionary.confirm(
        "Apenas vagas onde tenho conexões?", default=False, style=custom_style
    ).ask()

    if in_your_network is None:
        return None

    # Page number
    page_number = get_page_number()

    return {
        "tech": tech,
        "exclude": exclude,
        "page_number": page_number,
        "filters": {
            "workplaceType": workplace_type,
            "experienceLevel": experience_level,
            "jobType": job_type,
            "datePosted": date_posted,
            "easyApply": easy_apply,
            "inYourNetwork": in_your_network,
        },
    }


def collect_content_search_data():
    """Collect content search parameters from user."""
    print("\n🔎 LinkedIn Query Helper - Busca de Publicações\n")

    # Technology
    tech = questionary.autocomplete(
        "Tecnologia/palavra-chave:", choices=TECH_SUGGESTIONS, style=custom_style
    ).ask()

    if not tech:
        return None

    # Exclude keywords
    exclude = get_exclude_keywords()

    # Page number
    page_number = get_page_number()

    return {"tech": tech, "exclude": exclude, "page_number": page_number}


def main():
    """Main CLI entry point."""
    while True:
        print("\n" + "=" * 50)
        print("🔎  LinkedIn Query Helper")
        print("=" * 50 + "\n")

        # Select search type
        search_type = questionary.select(
            "Buscar em:",
            choices=[
                questionary.Choice("Vagas", value="jobs"),
                questionary.Choice("Publicações", value="content"),
                questionary.Choice("Sair", value="exit"),
            ],
            style=custom_style,
        ).ask()

        if search_type == "exit" or search_type is None:
            print("\n👋 Até logo!\n")
            break

        # Collect search data
        if search_type == "jobs":
            data = collect_job_search_data()
            if not data:
                continue
            url = build_job_search_url(
                data["tech"], data["page_number"], data["exclude"], data["filters"]
            )
        else:  # content
            data = collect_content_search_data()
            if not data:
                continue
            url = build_content_search_url(
                data["tech"], data["page_number"], data["exclude"]
            )

        # Show URL and open browser
        print("\n" + "=" * 50)
        print("✅ URL gerada com sucesso!")
        print("=" * 50)
        print(f"\n{url}\n")
        print("🌐 Abrindo no navegador...\n")

        webbrowser.open(url)

        # Ask if user wants to continue
        continue_search = questionary.confirm(
            "Fazer outra busca?", default=True, style=custom_style
        ).ask()

        if not continue_search:
            print("\n👋 Até logo!\n")
            break


if __name__ == "__main__":
    main()
