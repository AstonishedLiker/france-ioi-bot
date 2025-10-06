from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from france_ioi.Level import Level
    from france_ioi.Task import Task

class Chapter():
    def __init__(self, title: str, link: str, parent: Level):
        self.title = title
        self.link = link
        self.parent = parent
        self.tasks: list[Task] = []
