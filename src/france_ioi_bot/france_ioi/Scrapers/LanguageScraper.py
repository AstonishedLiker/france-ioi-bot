from typing import Optional
from bs4 import BeautifulSoup
from france_ioi.Language import Language

def scrape_language(doc: BeautifulSoup) -> Optional[Language]:
    languageDiv = doc.find("div", { "class": "menu-language-select" })
    if languageDiv is None:
        print(":: Error scrapping the France-IOI home page, cannot find the language div")
        return None

    languageListDiv = languageDiv.div
    assert languageListDiv is not None

    languageImg = languageListDiv.img
    assert languageImg is not None

    languageTitle = languageImg["title"]
    return Language(languageTitle)