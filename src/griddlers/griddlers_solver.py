from collections import deque
from typing import List

from griddlers.cell_mark import CellsLine
from griddlers.griddlers_game import GriddlersGame
from griddlers.line_solve_strategies import (
    CompletionIdentificationStrategy, EdgeStrategy, OverlapStrategy
)


class GriddlersSolver:

    def __init__(self):
        self.strategies = [
            OverlapStrategy(), EdgeStrategy(), CompletionIdentificationStrategy()
        ]

    def solve(self, game: GriddlersGame):
        rows_queue, columns_queue = self.get_rows_and_columns_queues(game)
        while (
            (len(rows_queue) != 0 or len(columns_queue) != 0)
            and not game.is_complete
        ):
            while len(rows_queue) != 0:
                row_index = rows_queue.pop()
                row, row_instructions = game.get_row_and_instructions(
                    row_index=row_index
                )
                result_row = self.run_strategies(row, row_instructions)
                differ_indices = self.calculate_differ_indices(row, result_row)
                if len(differ_indices) != 0:
                    game.set_row(row_index=row_index, row=result_row)
                    rows_queue.appendleft(row_index)
                    for i in differ_indices:
                        columns_queue.appendleft(i)
            while len(columns_queue) != 0:
                column_index = columns_queue.pop()
                column, column_instructions = game.get_column_and_instructions(
                    column_index=column_index
                )
                result_column = self.run_strategies(column, column_instructions)
                differ_indices = self.calculate_differ_indices(column, result_column)
                if len(differ_indices) != 0:
                    game.set_column(column_index=column_index, column=result_column)
                    columns_queue.appendleft(column_index)
                    for i in differ_indices:
                        rows_queue.appendleft(i)

    def run_strategies(self, line: CellsLine, instructions: List[int]):
        for strategy in self.strategies:
            line = strategy.solve(line=line, instructions=instructions)
        return line

    @classmethod
    def get_rows_and_columns_queues(cls, game):
        rows_queue = deque()
        columns_queue = deque()
        for i in range(game.rows):
            rows_queue.appendleft(i)
        for i in range(game.columns):
            columns_queue.appendleft(i)
        return rows_queue, columns_queue

    @classmethod
    def calculate_differ_indices(cls, line1: CellsLine, line2: CellsLine):
        return [i for i, (val1, val2) in enumerate(zip(line1, line2)) if val1 != val2]