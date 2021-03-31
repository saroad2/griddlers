from dataclasses import dataclass, field
from typing import List, Union

from griddlers.cell_mark import CellMark
from griddlers.cells_section import CellsSection


class CellsLine(list):

    cells: List[CellMark] = field(default_factory=list)
    
    def __init__(self, items: List[CellMark] = None):
        super().__init__(items)
        
    @classmethod
    def parse_line(cls, line: str) -> "CellsLine":
        return CellsLine([CellMark(val) for val in line])

    @property
    def is_completed(self):
        return all(cell != CellMark.EMPTY for cell in self)

    @property
    def sections(self):
        sections = []
        if len(self) == 0:
            return sections
        start_index = 0
        mark = self[0]
        for i in range(1, len(self)):
            if self[i] != mark:
                sections.append(CellsSection(start=start_index, end=i - 1, mark=mark))
                start_index = i
                mark = self[i]
        sections.append(
            CellsSection(start=start_index, end=len(self) - 1, mark=mark)
        )
        return sections

    @property
    def filled_sections(self):
        return [section for section in self.sections if section.mark == CellMark.FILLED]

    @property
    def empty_sections(self):
        return [section for section in self.sections if section.mark == CellMark.EMPTY]

    def inverse(self) -> "CellsLine":
        return CellsLine(self[::-1])

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, slice):
            return CellsLine(super().__getitem__(key))
        return super().__getitem__(key)

    def __repr__(self):
        return "".join(cell.value for cell in self)

    def __eq__(self, other):
        if not isinstance(other, CellsLine):
            return False
        return super().__eq__(other)
