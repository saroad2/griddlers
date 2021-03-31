from dataclasses import dataclass, field

from griddlers.cell_mark import CellMark


@dataclass
class CellsSection:

    start: int
    end: int
    mark: CellMark
    blocked_below: bool = field(default=False)
    blocked_above: bool = field(default=False)

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(
                "Cannot create section with end smaller than start "
                f"({self.end} < {self.start}"
            )

    @property
    def length(self):
        return self.end - self.start + 1

    @property
    def blocked(self):
        return self.blocked_below and self.blocked_above

    def __contains__(self, index):
        return self.start <= index <= self.end

    def __iter__(self):
        return iter(range(self.start, self.end + 1))
