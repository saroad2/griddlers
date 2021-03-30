from griddlers.cells_line import CellsLine
from griddlers.cell_mark import CellMark


class GriddlersBoard:

    def __init__(
        self, rows: int, columns: int
    ):
        self.rows = rows
        self.columns = columns
        self.cells_map = dict()
        self.clear()

    @property
    def is_completed(self) -> bool:
        return all(self.get_row(i).is_completed for i in range(self.rows))

    def get_row(self, row_index: int) -> CellsLine:
        return CellsLine(
            cells=[
                self[(row_index, j)] for j in range(self.columns)
            ]
        )

    def set_row(self, row_index: int, row: CellsLine):
        for column_index, val in enumerate(row):
            self[row_index, column_index] = val

    def get_column(self, column_index: int) -> CellsLine:
        return CellsLine(
            cells=[
                self[(j, column_index)] for j in range(self.rows)
            ]
        )

    def set_column(self, column_index: int, column: CellsLine):
        for row_index, val in enumerate(column):
            self[row_index, column_index] = val

    def clear(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self[i, j] = CellMark.EMPTY

    def __getitem__(self, key):
        return self.cells_map[key]

    def __setitem__(self, key, value):
        row, col = key
        if row < 0 or row >= self.rows:
            raise ValueError(
                f"Row number should be between 0 and {self.rows - 1}. Got {row}"
            )
        if col < 0 or col >= self.columns:
            raise ValueError(
                f"Column number should be between 0 and {self.columns - 1}. Got {col}"
            )
        if not isinstance(value, CellMark):
            raise ValueError(f"Can only set marks on board. Got {value}")
        self.cells_map[key] = value

    def __repr__(self):
        return "\n".join(str(self.get_row(i)) for i in range(self.rows))
