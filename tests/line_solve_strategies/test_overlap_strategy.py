from pytest_cases import parametrize_with_cases
from griddlers.cell_mark import CellsLine
from griddlers.line_solve_strategies import OverlapStrategy


def case_one_instruction_overlap():
    line = "_______"
    instructions = [5]
    result_line = "__OOO__"

    return line, instructions, result_line


def case_one_instruction_full_line():
    line = "_____"
    instructions = [5]
    result_line = "OOOOO"

    return line, instructions, result_line


def case_two_instructions_one_overlap():
    line = "_______"
    instructions = [1, 3]
    result_line = "____O__"

    return line, instructions, result_line


def case_two_instructions_two_overlaps():
    line = "_______"
    instructions = [2, 3]
    result_line = "_O__OO_"

    return line, instructions, result_line


def case_one_instruction_with_cross_overlap():
    line = "_X_____"
    instructions = [4]
    result_line = "_X_OOO_"

    return line, instructions, result_line


def case_two_instructions_with_filled_blocks():
    line = "___OO_______"
    instructions = [3, 4]
    result_line = "___OO___OO__"

    return line, instructions, result_line


@parametrize_with_cases(argnames=["line", "instructions", "result_line"], cases=".")
def test_overlap_strategy(line, instructions, result_line):
    overlap_strategy = OverlapStrategy()

    input_line = CellsLine.parse_line(line)
    actual_result = overlap_strategy.solve(line=input_line, instructions=instructions)
    expected_result = CellsLine.parse_line(result_line)

    assert actual_result == expected_result
    if line != result_line:
        assert actual_result != input_line
