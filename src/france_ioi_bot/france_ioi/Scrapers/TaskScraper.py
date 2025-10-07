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
        print(f"!! Warning scrapping the France-IOI chapter page: cannot find the exercises body div ({chapter.link})\n\t- NOTE: 'Programmer sur un ordinateur' is NOT supported yet")
        return False

    for exerciseDiv in exercises.find_all("div", recursive=False):
        categorySpan = exerciseDiv.find("span", { "class": "chapter-item-category" })
        assert categorySpan is not None

        categoryTextSpan = categorySpan.span
        assert categoryTextSpan is not None

        category = categoryTextSpan["class"]
        titleSpan = exerciseDiv.find("span", { "class": "chapter-item-title" })
        assert titleSpan is not None

        anchor = titleSpan.a
        assert anchor is not None

        taskTitle = anchor.get_text()
        link = anchor["href"]
        assert isinstance(link, str)

        stateImg = exerciseDiv.img
        assert stateImg is not None

        stateTitle = stateImg["title"]
        assert isinstance(stateTitle, str)

        isFinished = stateTitle.startswith("Terminé")
        chapter.tasks.append(Task(taskTitle, link, isFinished, TaskCategory(category[0]), chapter))

    return True