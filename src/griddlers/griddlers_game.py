import json
from pathlib import Path
from typing import List, Union

from griddlers.cells_line import CellsLine
from griddlers.griddlers_board import GriddlersBoard


class GriddlersGame:

    def __init__(
        self, rows_instructions: List[List[int]], columns_instructions: List[List[int]]
    ):
        self.rows_instructions = rows_instructions
        self.columns_instructions = columns_instructions
        self.board = GriddlersBoard(
            rows=len(self.rows_instructions), columns=len(self.columns_instructions)
        )

    @property
    def rows(self):
        return self.board.rows

    @property
    def columns(self):
        return self.board.columns

    @property
    def is_complete(self):
        return self.board.is_completed

    @property
    def is_won(self):
        for row, row_instructions in self.iterate_rows():
            if [section.length for section in row.filled_sections] != row_instructions:
                return False
        for column, column_instructions in self.iterate_columns():
            if [
                section.length for section in column.filled_sections
            ] != column_instructions:
                return False
        return True

    def get_row_and_instructions(self, row_index: int):
        return self.board.get_row(row_index), self.rows_instructions[row_index]

    def get_column_and_instructions(self, column_index: int):
        return (
            self.board.get_column(column_index), self.columns_instructions[column_index]
        )

    def iterate_rows(self):
        for i in range(self.rows):
            yield self.get_row_and_instructions(i)

    def iterate_columns(self):
        for i in range(self.rows):
            yield self.get_row_and_instructions(i)

    def set_row(self, row_index: int, row: CellsLine):
        self.board.set_row(row_index=row_index, row=row)

    def set_column(self, column_index: int, column: CellsLine):
        self.board.set_column(column_index=column_index, column=column)

    def clear(self):
        self.board.clear()

    @classmethod
    def load_from_file(cls, path: Union[str, Path]) -> "GriddlersGame":
        with open(path, mode="r") as pd:
            data = json.load(pd)
        return GriddlersGame(**data)

    def board_string(self):
        return str(self.board)
