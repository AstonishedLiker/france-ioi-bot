from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from france_ioi.Chapter import Chapter

class TaskCategory(Enum):
    DISCOVERY = "CategoryDiscovery"
    COURSE = "CategoryCourse"
    APPLICATION = "CategoryApplication"
    VALIDATION = "CategoryValidation"
    CHALLENGE = "CategoryChallenge"

class Task():
    def __init__(self, title: str, link: str, isFinished: bool, category: TaskCategory, parent: Chapter):
        self.title = title
        self.link = link
        self.isFinished = isFinished
        self.category = category
        self.parent = parent
