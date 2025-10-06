from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from france_ioi.Chapter import Chapter

class Level():
    def __init__(self, title: str, locked: bool):
        self.title = title
        self.locked = locked
        self.chapters: list[Chapter] = []
