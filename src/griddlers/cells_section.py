from dataclasses import dataclass

from griddlers.cell_mark import CellMark


@dataclass
class CellsSection:

    start: int
    end: int
    mark: CellMark

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(
                "Cannot create section with end smaller than start "
                f"({self.end} < {self.start}"
            )

    @property
    def length(self):
        return self.end - self.start + 1

    def __contains__(self, index):
        return self.start <= index <= self.end

    def __iter__(self):
        return iter(range(self.start, self.end + 1))
