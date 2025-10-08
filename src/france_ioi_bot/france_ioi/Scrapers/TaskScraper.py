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
    response = account.getHttpQueryAuthed(chapter.link.removeprefix(FRANCEIOI_BASE_URL))
    if response is None:
        return False

    doc = BeautifulSoup(response.content.decode(), "html.parser")
    taskListDiv = doc.find("div", { "class": "chapter-tasks" })
    if taskListDiv is None:
        print(f"!! Cannot find tasks for chapter '{chapter.title}' ({chapter.link})")
        return False

    for taskDiv in taskListDiv.find_all("div", { "class": "chapter-item-row" }):
        titleSpan = taskDiv.find("span", { "class": "chapter-item-title" })
        assert titleSpan is not None

        anchor = titleSpan.a
        assert anchor is not None

        taskTitle = anchor.get_text()
        link = anchor["href"]
        assert isinstance(link, str)

        categorySpan = taskDiv.find("span", { "class": "chapter-item-category" })
        if categorySpan:
            categoryTextSpan = categorySpan.span
            assert categoryTextSpan is not None
            assert categoryTextSpan["class"] is not None
            categoryStr: str = categoryTextSpan["class"][0]
            category = TaskCategory(categoryStr)
        else:
            chapterItemType = doc.find("img", { "class": "chapter-item-type" })
            if chapterItemType is None:
                print(f"!! Cannot find task type for chapter '{chapter.title}' ({chapter.link})")
                continue
            titleType = chapterItemType["title"]
            if titleType == "Cours":
                category = TaskCategory("CategoryCourse")
            elif titleType == "Sujet":
                category = TaskCategory("CategoryValidation")
            else:
                print(f"!! Unknown chapter item type '{chapterItemType['title']}' for chapter '{chapter.title}' ({chapter.link})")
                continue

        stateImg = taskDiv.find("img", { "class": "chapter-item-state" })
        assert stateImg is not None

        stateTitle = stateImg["title"]
        assert isinstance(stateTitle, str)

        isFinished = stateTitle.startswith("Lu") if category == TaskCategory.COURSE else stateTitle.startswith("Terminé")
        chapter.tasks.append(Task(taskTitle, link, isFinished, category, chapter))

    return True