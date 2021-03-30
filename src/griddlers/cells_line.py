from dataclasses import dataclass, field
from typing import List

from griddlers.cell_mark import CellMark


@dataclass(repr=False)
class CellsLine:

    cells: List[CellMark] = field(default_factory=list)

    @classmethod
    def parse_line(cls, line: str) -> "CellsLine":
        return CellsLine(cells=[CellMark(val) for val in line])

    @property
    def is_completed(self):
        return all(cell != CellMark.EMPTY for cell in self.cells)

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