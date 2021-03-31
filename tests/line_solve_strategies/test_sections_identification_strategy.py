from pytest_cases import parametrize_with_cases
from griddlers.cells_line import CellsLine
from griddlers.line_solve_strategies import SectionsIdentificationStrategy


def case_full_line():
    line = "OOOOO"
    instructions = [5]
    result_line = "OOOOO"

    return line, instructions, result_line


def case_one_full_instruction_in_start():
    line = "OOO__"
    instructions = [3]
    result_line = "OOOXX"

    return line, instructions, result_line


def case_one_partial_instruction_in_start():
    line = "OO___"
    instructions = [3]
    result_line = "OO_XX"

    return line, instructions, result_line


def case_one_full_instruction_in_end():
    line = "__OOO"
    instructions = [3]
    result_line = "XXOOO"

    return line, instructions, result_line


def case_one_partial_instruction_in_end():
    line = "___OO"
    instructions = [3]
    result_line = "XX_OO"

    return line, instructions, result_line


def case_one_full_instruction_in_middle():
    line = "___OO__"
    instructions = [2]
    result_line = "XXXOOXX"

    return line, instructions, result_line


def case_one_partial_instruction_in_middle():
    line = "___OO__"
    instructions = [3]
    result_line = "XX_OO_X"

    return line, instructions, result_line


def case_two_full_instructions_in_middle():
    line = "_OO_O_"
    instructions = [2, 1]
    result_line = "XOOXOX"

    return line, instructions, result_line


def case_two_partial_instructions_in_middle_with_middle_space():
    line = "__O____O___"
    instructions = [2, 3]
    result_line = "X_O_X__O__X"

    return line, instructions, result_line


def case_two_partial_instructions_in_middle_without_middle_space():
    line = "__O___O___"
    instructions = [2, 3]
    result_line = "X_O___O__X"

    return line, instructions, result_line


def case_two_partial_instructions_in_middle_with_overlapping_gap():
    line = "__O__O___"
    instructions = [2, 3]
    result_line = "X_O__O__X"

    return line, instructions, result_line


def case_two_partial_instructions_no_change():
    line = "__O_O____"
    instructions = [3, 3]
    result_line = "__O_O____"

    return line, instructions, result_line


@parametrize_with_cases(argnames=["line", "instructions", "result_line"], cases=".")
def test_sections_identification_strategy(line, instructions, result_line):
    sections_identification_strategy = SectionsIdentificationStrategy()

    input_line = CellsLine.parse_line(line)
    actual_result = sections_identification_strategy.solve(
        line=input_line, instructions=instructions
    )
    expected_result = CellsLine.parse_line(result_line)

    assert actual_result == expected_result
    if line != result_line:
        assert actual_result != input_line
