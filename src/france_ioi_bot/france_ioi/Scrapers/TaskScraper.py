from __future__ import annotations
from bs4 import BeautifulSoup
from typing import TYPE_CHECKING
from france_ioi.Task import Task
from france_ioi.Chapter import Chapter
from france_ioi.Task import TaskCategory
from france_ioi.Constants import FRANCEIOI_BASE_URL

if TYPE_CHECKING:
    from france_ioi.Account import Account

def scrape_tasks(account: Account, chapter: Chapter) -> bool:
    response = account.httpQueryAuthed(chapter.link.removeprefix(FRANCEIOI_BASE_URL))
    if response is None:
        return False
    doc = BeautifulSoup(response.content.decode(), "html.parser")
    exercises = doc.find("div", { "class": "chapter-tasks with-categories" })
    if exercises is None:
        print(f":: Warning scrapping the France-IOI chapter page: cannot find the exercises body div ({chapter.link})\n\t- NOTE: 'Programmer sur un ordinateur' is NOT supported")
        return False

    for exerciseDiv in exercises.find_all("div", recursive=False):
        category = exerciseDiv.find("span", { "class": "chapter-item-category" }).span["class"]
        anchor = exerciseDiv.find("span", { "class": "chapter-item-title" }).a

        title = anchor.get_text()
        link = anchor["href"]
        isFinished = exerciseDiv.img["title"].startswith("Terminé")

        chapter.tasks.append(Task(title, link, isFinished, TaskCategory(category[0]), chapter))

    return True