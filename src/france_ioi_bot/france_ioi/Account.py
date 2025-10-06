from typing import Optional
from requests import Session, Response
from bs4 import BeautifulSoup

from france_ioi.Level import scrape_levels

FRANCEIOI_BASE_URL = "https://www.france-ioi.org"

class Account():
    def __init__(self, phpSessId: str):
        self.session = Session()
        self.hasSuccessfullyInitialized = False
        self.username: Optional[str] = None
        self.session.cookies["PHPSESSID"] = phpSessId
        self.initialize()

    def _httpQuery(self, subdomain: str) -> Optional[Response]:
        response = self.session.get(FRANCEIOI_BASE_URL + subdomain)
        if response.status_code != 200:
            print(f":: Error querying France-IOI: expecting status code 200, got {response.status_code})!")
            return None
        return response

    def initialize(self) -> bool:
        assert self.hasSuccessfullyInitialized == False

        response = self._httpQuery(f"/algo/chapters.php")
        if response is None:
            return False

        doc = BeautifulSoup(str(response.content), "html.parser")
        label = doc.find("label", { "for": "menuLoginToggle" })
        if label is None:
            print(":: Error scrapping the France-IOI home page: cannot find local user label")
            return False

        username = label.getText()
        if username == "Connexion":
            print(":: Error logging in France-IOI: Invalid PHPSESSID token")
            return False

        self.username = username
        self.hasSuccessfullyInitialized = True

        return True

    def queryLevels(self):
        response = self._httpQuery(f"/algo/chapters.php")
        if response is None:
            return None

        return scrape_levels(str(response.content))
