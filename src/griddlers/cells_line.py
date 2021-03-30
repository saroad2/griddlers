from dataclasses import dataclass, field
from typing import List

from griddlers.cell_mark import CellMark
from griddlers.cells_section import CellsSection


@dataclass(repr=False)
class CellsLine:

    cells: List[CellMark] = field(default_factory=list)

    @classmethod
    def parse_line(cls, line: str) -> "CellsLine":
        return CellsLine(cells=[CellMark(val) for val in line])

    @property
    def is_completed(self):
        return all(cell != CellMark.EMPTY for cell in self.cells)

    @property
    def sections(self):
        sections = []
        if len(self.cells) == 0:
            return sections
        start_index = 0
        mark = self.cells[0]
        for i in range(1, len(self.cells)):
            if self.cells[i] != mark:
                sections.append(CellsSection(start=start_index, end=i - 1, mark=mark))
                start_index = i
                mark = self.cells[i]
        sections.append(
            CellsSection(start=start_index, end=len(self.cells) - 1, mark=mark)
        )
        return sections

    @property
    def filled_sections(self):
        return [section for section in self.sections if section.mark == CellMark.FILLED]

    @property
    def empty_sections(self):
        return [section for section in self.sections if section.mark == CellMark.EMPTY]

    def inverse(self) -> "CellsLine":
        return CellsLine(cells=self.cells[::-1])

    def __getitem__(self, index: int):
        return self.cells[index]

    def __setitem__(self, index: int, value: CellMark):
        self.cells[index] = value

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return "".join(cell.value for cell in self.cells)