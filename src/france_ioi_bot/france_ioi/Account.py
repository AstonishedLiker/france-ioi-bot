from bs4 import BeautifulSoup
from typing import Optional
import requests

from france_ioi.Scrapers.ChapterLevelScraper import scrape_levels_chapters
from france_ioi.Scrapers.UsernameScraper import scrape_username
from france_ioi.Scrapers.LanguageScraper import scrape_language
from france_ioi.Language import Language
from france_ioi.Constants import FRANCEIOI_BASE_URL

class Account():
    def __init__(self, phpSessId: str):
        self.phpSessId = phpSessId
        self.session: requests.Session = requests.Session()
        self.session.cookies.set("PHPSESSID", phpSessId)
        self.hasSuccessfullyInitialized = False
        self.username: Optional[str] = None
        self.initialize()

    def initialize(self):
        assert not self.hasSuccessfullyInitialized

        response = self.getHttpQueryAuthed(f"/algo/chapters.php", True)
        if response is None:
            return

        doc = BeautifulSoup(response.content.decode(), "html.parser")
        language = scrape_language(doc)
        if language is not None and language != Language.FRENCH:
            print(":: Please set your language to french in the France-IOI user interface")
            return
        elif language is None:
            return

        self.username = scrape_username(doc)
        self.hasSuccessfullyInitialized = isinstance(self.username, str)

    def getHttpQueryAuthed(self, subdomain: str, bypassInitCheck: bool = False) -> Optional[requests.Response]:
        if not bypassInitCheck:
            assert self.hasSuccessfullyInitialized

        response = self.session.get(FRANCEIOI_BASE_URL + subdomain)
        if not response.ok:
            print(f":: Error GET France-IOI ({subdomain}), expecting success, got error code {response.status_code})")
            return None
        return response

    def postHttpQueryAuthed(self, subdomain: str, data: dict) -> Optional[requests.Response]:
        assert self.hasSuccessfullyInitialized

        response = self.session.post(FRANCEIOI_BASE_URL + subdomain, data=data)
        if response.status_code not in [200, 201, 204]:
            print(f":: Error POST France-IOI ({subdomain}), expecting success, got error code {response.status_code})")
            return None
        return response

    def queryLevels(self):
        assert self.hasSuccessfullyInitialized

        response = self.getHttpQueryAuthed(f"/algo/chapters.php")
        if response is None:
            return None

        return scrape_levels_chapters(self, response.content.decode())
