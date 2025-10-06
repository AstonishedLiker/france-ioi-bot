from __future__ import annotations
import re
from typing import Optional, TYPE_CHECKING
from bs4 import BeautifulSoup
from bs4.element import Tag
from france_ioi.Chapter import Chapter
from france_ioi.Level import Level
from france_ioi.Scrapers.TaskScraper import scrape_tasks

if TYPE_CHECKING:
    from france_ioi.Account import Account

# TODO: Simplify error handling, if not removing most of it altogether (some guarentees are always ensured)
def scrape_levels_chapters(account: Account, html_doc: str) -> Optional[list[Level]]:
    doc = BeautifulSoup(html_doc, "html.parser")
    levelTable = doc.find("table", { "class": "chapters-list" })
    if levelTable is None:
        print(":: Error scrapping the France-IOI home page: cannot find the chapters body table")
        return None

    levelTableBody: Tag = levelTable.tbody
    assert levelTableBody is not None # This should never happen

    levels: list[Level] = []
    currentLevel: Optional[Level] = None

    for child in levelTableBody.find_all("tr"):
        if "chapters-category" in child.td.get("class", []):
            levelHeading = child.td.h2
            if levelHeading is None:
                print(":: Error scrapping the France-IOI home page: title missing from level")
                return None

            text = levelHeading.get_text(strip=True) # France-IOI has a ton of weird whitespace for some reason??
            levelMatch = re.search(r'Niveau \d+', text)
            assert levelMatch is not None

            locked = re.search(r'\[Pour', text) is not None
            currentLevel = Level(levelMatch.group(0), locked=locked)
            levels.append(currentLevel)
        elif not currentLevel.locked: # So we don't add locked chapters, since we can't see them yet.
            anchor = child.find("a")
            if anchor is None:
                print(":: Error scrapping the France-IOI home page: anchor missing from chapter")
                return None
            assert currentLevel is not None # There should always be a level before a chapter
            chapterLink = anchor["href"]
            assert isinstance(chapterLink, str)
            currentLevel.chapters.append(Chapter(anchor.get_text(strip=True), chapterLink, currentLevel))

    for level in levels:
        if level.locked:
            break
        for chapter in level.chapters:
            scrape_tasks(account, chapter)

    assert len(levels) > 0 # There should be at least one level
    return levels
