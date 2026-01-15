import requests
from bs4 import BeautifulSoup


def get_url(
    url: str, compact=True, remove_classes=False, remove_ids=False, remove_styles=False
):
    response = requests.get(url)
    html = response.text

    if any([remove_classes, remove_ids, remove_styles]):
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all(True):
            if remove_classes and tag.has_attr("class"):
                del tag["class"]
            if remove_ids and tag.has_attr("id"):
                del tag["id"]
            if remove_styles and tag.has_attr("style"):
                del tag["style"]

        html = str(soup)

    return html


def compact(html):
    html = "\n".join(line for line in html.split("\n") if line.strip())
    return html


def conveter_markdown(html):
    print()


def main():
    html = get_url(
        "https://docs.astral.sh/ty/installation/",
        compact=True,
        remove_classes=True,
        remove_ids=True,
        remove_styles=True,
    )
    print(compact(html))


if __name__ == "__main__":
    main()
