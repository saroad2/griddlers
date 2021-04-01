from copy import deepcopy
from typing import List

from griddlers.cells_line import CellsLine
from griddlers.cell_mark import CellMark
from griddlers.cells_section import CellsSection


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
            line.mark_inclusive(start_index, end_index, CellMark.FILLED)
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
            while line[line_index] == CellMark.CROSSED:
                line_index += 1
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


class SectionsIdentificationStrategy(GriddlersLineSolveStrategy):

    def __init__(self):
        super().__init__(one_way=True)

    def solve_one_way(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        filled_sections = line.filled_sections
        if len(filled_sections) != len(instructions):
            return line
        for i in range(0, len(filled_sections) - 1):
            section, next_section = filled_sections[i], filled_sections[i + 1]
            instruction, next_instruction = instructions[i], instructions[i + 1]
            if not self.splitted_sections(
                line=line,
                section=section,
                next_section=next_section,
                instruction=instruction,
                next_instruction=next_instruction,
            ):
                return line

        for i in range(0, len(filled_sections) - 1):
            section, next_section = filled_sections[i], filled_sections[i + 1]
            instruction, next_instruction = instructions[i], instructions[i + 1]
            cross_start = section.end + instruction - section.length + 1
            cross_end = next_section.start - next_instruction + next_section.length - 1
            line.mark_inclusive(cross_start, cross_end, CellMark.CROSSED)
        first_section, last_section = filled_sections[0], filled_sections[-1]
        first_instruction, last_instruction = instructions[0], instructions[-1]
        first_cross_end = first_section.start - first_instruction + first_section.length - 1
        if 0 <= first_cross_end < first_section.start:
            line.mark_inclusive(0, first_cross_end, CellMark.CROSSED)
        last_cross_start = last_section.end + last_instruction - last_section.length + 1
        if last_section.end < last_cross_start < len(line):
            line.mark_inclusive(last_cross_start, len(line) - 1, CellMark.CROSSED)
        return line

    def splitted_sections(
        self,
        line: CellsLine,
        section: CellsSection,
        next_section: CellsSection,
        instruction: int,
        next_instruction: int,
    ):
        if CellMark.CROSSED in line[section.end + 1: next_section.start - 1]:
            return True
        gap = next_section.start - section.end - 1
        return (
            gap >= instruction - section.length
            and gap >= next_instruction - next_section.length
        )


class MaxSectionIdentifierStrategy(GriddlersLineSolveStrategy):

    def __init__(self):
        super().__init__(one_way=True)

    def solve_one_way(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        known_sections_sizes = [
            section.length for section in line.filled_sections if section.blocked
        ]
        remaining_instructions = list(instructions)
        for instruction in known_sections_sizes:
            remaining_instructions.remove(instruction)
        if len(remaining_instructions) == 0:
            return line
        max_instruction = max(remaining_instructions)
        for section in line.filled_sections:
            if section.length != max_instruction:
                continue
            if not section.blocked_below:
                line[section.start - 1] = CellMark.CROSSED
            if not section.blocked_above:
                line[section.end + 1] = CellMark.CROSSED
        return line


class GapsFillerStrategy(GriddlersLineSolveStrategy):

    def __init__(self):
        super().__init__(one_way=False)

    def solve_one_way(self, line: CellsLine, instructions: List[int]) -> CellsLine:
        if line.is_completed:
            return line
        first_empty_section = line.empty_sections[0]
        if (
            first_empty_section.start != 0
            and line[first_empty_section.start - 1] == CellMark.FILLED
        ):
            return line
        number_of_known_instructions = len(
            [
                section for section in line.filled_sections
                if section.end < first_empty_section.start
            ]
        )
        remaining_instructions = instructions[number_of_known_instructions:]
        if len(remaining_instructions) == 0:
            return line
        first_remaining_instruction = remaining_instructions[0]
        min_remaining_instruction = min(remaining_instructions)
        remaining_sections = [
            section for section in line.sections
            if section.start >= first_empty_section.start
        ]
        fill_first_gap = True
        for i in range(len(remaining_sections)):
            section = remaining_sections[i]
            if section.mark == CellMark.FILLED:
                if not fill_first_gap:
                    continue
                fill_first_gap = False
                previous_section = remaining_sections[i - 1]
                if (
                    previous_section.mark == CellMark.EMPTY
                    and previous_section.length < first_remaining_instruction
                ):
                    line.mark_inclusive(
                        section.start,
                        previous_section.start + first_remaining_instruction - 1,
                        CellMark.FILLED
                    )
                continue
            if section.mark == CellMark.CROSSED:
                continue
            if not section.blocked:
                continue
            if section.length >= first_remaining_instruction:
                fill_first_gap = False
            if (
                section.length < min_remaining_instruction
                or (fill_first_gap and section.length < first_remaining_instruction)
            ):
                line.mark_inclusive(section.start, section.end, CellMark.CROSSED)
        return line
