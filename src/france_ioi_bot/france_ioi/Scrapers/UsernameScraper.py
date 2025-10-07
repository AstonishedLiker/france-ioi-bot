from bs4 import BeautifulSoup
from typing import Optional

def scrape_username(doc: BeautifulSoup) -> Optional[str]:
    label = doc.find("label", { "for": "menuLoginToggle" })
    assert label is not None

    username = label.get_text()
    if username == "Connexion":
        print(":: Error logging in France-IOI: Invalid PHPSESSID token")
        return None

    return username
