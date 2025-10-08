from __future__ import annotations
from bs4 import BeautifulSoup
from typing import TYPE_CHECKING
from france_ioi.Task import Task
from france_ioi.Chapter import Chapter
from france_ioi.Task import TaskCategory
from france_ioi.Constants import FRANCEIOI_BASE_URL

if TYPE_CHECKING:
    from france_ioi.Account import Account

async def scrape_tasks(account: Account, chapter: Chapter) -> bool:
    response = account.getHttpQueryAuthed(chapter.link.removeprefix(FRANCEIOI_BASE_URL))
    if response is None:
        return False
    doc = BeautifulSoup(response.content.decode(), "html.parser")
    exercises = doc.find("div", { "class": "chapter-tasks with-categories" })
    if exercises is None:
        print(f"!! Cannot find the exercises body div, the chapter may not be supported ({chapter.link})")
        return False

    for exerciseDiv in exercises.find_all("div", { "class": "chapter-item-row" }):
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

        category = TaskCategory(category[0])
        isFinished = stateTitle.startswith("Lu") if category == TaskCategory.COURSE else stateTitle.startswith("Terminé")

        chapter.tasks.append(Task(taskTitle, link, isFinished, category, chapter))

    return True