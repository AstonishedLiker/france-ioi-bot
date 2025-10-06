from typing import Optional
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

FRANCEIOI_BASE_URL = "https://www.france-ioi.org"

class Level():
    def __init__(self, title: str):
        self.title = title
        self.levels = []

def scrape_levels(html_doc: str) -> Optional[list[Level]]:
    doc = BeautifulSoup(html_doc, "html.parser")
    levelTable = doc.find("table", { "class": "chapters-list" })
    if levelTable is None:
        print(":: Error scrapping the France-IOI home page: cannot find the chapters body table")
        return None

    levelTableBody: PageElement = levelTable.contents[0] # type: ignore[reportUnknownMemberType]
    assert levelTableBody is not None # This should never happen

    levels: list[Level] = []
    for child in levelTableBody.children: # type: ignore[reportUnknownMemberType]
        firstElement: Optional[Tag] = child.contents.get(0) # type: ignore[reportUnknownMemberType]
        if firstElement is None:
            print(":: Error scrapping the France-IOI home page: children missing from tr element")
            return None
        if firstElement["class"] == "chapters-category":
            levelHeading = firstElement.find("h2")
            if levelHeading is None:
                print(":: Error scrapping the France-IOI home page: title missing from level")
                return None
            levels.append(Level(levelHeading.getText()))

    return levels