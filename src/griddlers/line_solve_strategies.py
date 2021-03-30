from copy import deepcopy
from typing import List

from griddlers.cells_line import CellsLine
from griddlers.cell_mark import CellMark


class GriddlersLineSolveStrategy:

    def __init__(self, one_way: bool):
        self.one_way = one_way

    def solve(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        line = self.solve_one_way(deepcopy(line), instructions)
        if not self.one_way:
            line = self.solve_one_way(line.inverse(), instructions[::-1]).inverse()
        return line

    def solve_one_way(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        raise NotImplementedError(
            "Please override GriddlersSolveStrategy.solve_one_way"
        )


class OverlapStrategy(GriddlersLineSolveStrategy):

    def __init__(self):
        super().__init__(one_way=True)

    def solve_one_way(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        number_of_instructions = len(instructions)
        for instruction_index in range(number_of_instructions):
            end_index = self.get_end_index(line, instructions, instruction_index)
            start_index = self.get_start_index(line, instructions, instruction_index)
            if start_index > end_index:
                continue
            for i in range(start_index, end_index + 1):
                line[i] = CellMark.FILLED
        return line

    def get_start_index(
        self, line: CellsLine, instructions: List[int], instruction_index: int
    ):
        inverted_index = self.get_end_index(
            line=line.inverse(),
            instructions=instructions[::-1],
            instruction_index=self.inverse_index(
                index=instruction_index, list_length=len(instructions)
            )
        )
        return self.inverse_index(inverted_index, len(line))

    def get_end_index(self, line, instructions, instruction_index):
        return self.combine_steps(line, instructions[:instruction_index + 1]) - 1

    @classmethod
    def combine_steps(cls, line: CellsLine, instructions: List[int]):
        line_index = 0
        instruction_index = 0
        while line_index < len(line) and instruction_index < len(instructions):
            instruction = instructions[instruction_index]
            bunch_size = 0
            while bunch_size < instruction:
                block_mark = line[line_index]
                if block_mark == CellMark.CROSSED:
                    bunch_size = 0
                else:
                    bunch_size += 1
                line_index += 1
            while line_index < len(line) and line[line_index] == CellMark.FILLED:
                line_index += 1
            if instruction_index != len(instructions) - 1:
                line_index += 1
            instruction_index += 1
        return line_index

    @classmethod
    def inverse_index(cls, index: int, list_length: int):
        return list_length - index - 1


class EdgeStrategy(GriddlersLineSolveStrategy):

    def __init__(self):
        super().__init__(one_way=False)

    def solve_one_way(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        line_index = 0
        for instruction in instructions:
            if line[line_index] != CellMark.FILLED:
                break
            block_size = 0
            while block_size < instruction:
                line[line_index] = CellMark.FILLED
                line_index += 1
                block_size += 1
            if line_index < len(line):
                line[line_index] = CellMark.CROSSED
            line_index += 1
        return line


class CompletionIdentificationStrategy(GriddlersLineSolveStrategy):

    def __init__(self):
        super().__init__(one_way=True)

    def solve_one_way(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        blocks_sizes = [section.length for section in line.filled_sections]
        if blocks_sizes != instructions:
            return line
        for section in line.empty_sections:
            for i in section:
                line[i] = CellMark.CROSSED
        return line

    @classmethod
    def get_block_size(cls, line: CellsLine, start_index: int):
        index = start_index
        while index < len(line) and line[index] == CellMark.FILLED:
            index += 1
        return index - start_index
