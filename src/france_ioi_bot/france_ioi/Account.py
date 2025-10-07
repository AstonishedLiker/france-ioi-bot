from bs4 import BeautifulSoup
from typing import Optional
from requests import Session, Response

from france_ioi.Scrapers.ChapterLevelScraper import scrape_levels_chapters
from france_ioi.Scrapers.UsernameScraper import scrape_username
from france_ioi.Scrapers.LanguageScraper import scrape_language
from france_ioi.Language import Language
from france_ioi.Constants import FRANCEIOI_BASE_URL

class Account():
    def __init__(self, phpSessId: str):
        self.session = Session()
        self.hasSuccessfullyInitialized = False
        self.username: Optional[str] = None
        self.session.cookies["PHPSESSID"] = phpSessId
        self.initialize()

    def getHttpQueryAuthed(self, subdomain: str) -> Optional[Response]:
        response = self.session.get(FRANCEIOI_BASE_URL + subdomain)
        if not response.ok:
            print(f":: Error GET France-IOI ({subdomain}): expecting success, got error code {response.status_code})!")
            return None
        return response

    def postHttpQueryAuthed(self, subdomain: str, data: dict) -> Optional[Response]:
        response = self.session.post(FRANCEIOI_BASE_URL + subdomain, data=data)
        if not response.ok:
            print(f":: Error POST France-IOI ({subdomain}): expecting success, got error code {response.status_code})!")
            return None
        return response

    # TODO: Check for language (as it will mess up the scraper)
    def initialize(self):
        assert self.hasSuccessfullyInitialized == False

        response = self.getHttpQueryAuthed(f"/algo/chapters.php")
        if response is None:
            return

        doc = BeautifulSoup(response.content.decode(), "html.parser")
        language = scrape_language(doc)
        if language is not None and language != Language.FRENCH:
            print(":: Please set your language to french in the France-IOI user interface!")
            return
        elif language is None:
            return

        self.username = scrape_username(doc)
        self.hasSuccessfullyInitialized = isinstance(self.username, str)

    def queryLevels(self):
        assert self.hasSuccessfullyInitialized

        response = self.getHttpQueryAuthed(f"/algo/chapters.php")
        if response is None:
            return None

        return scrape_levels_chapters(self, response.content.decode())
