from pytest_cases import parametrize_with_cases
from griddlers.cell_mark import CellsLine
from griddlers.line_solve_strategies import CompletionIdentificationStrategy


def case_full_line():
    line = "OOOOO"
    instructions = [5]
    result_line = "OOOOO"

    return line, instructions, result_line


def case_one_instruction_in_start():
    line = "OO___"
    instructions = [2]
    result_line = "OOXXX"

    return line, instructions, result_line


def case_one_instruction_in_end():
    line = "___OO"
    instructions = [2]
    result_line = "XXXOO"

    return line, instructions, result_line


def case_one_instruction_in_middle():
    line = "___OO__"
    instructions = [2]
    result_line = "XXXOOXX"

    return line, instructions, result_line


def case_two_instruction_in_middle():
    line = "_OO_O_"
    instructions = [2, 1]
    result_line = "XOOXOX"

    return line, instructions, result_line


@parametrize_with_cases(argnames=["line", "instructions", "result_line"], cases=".")
def test_completion_identification_strategy(line, instructions, result_line):
    completion_identification_strategy = CompletionIdentificationStrategy()

    input_line = CellsLine.parse_line(line)
    actual_result = completion_identification_strategy.solve(
        line=input_line, instructions=instructions
    )
    expected_result = CellsLine.parse_line(result_line)

    assert actual_result == expected_result
    if line != result_line:
        assert actual_result != input_line
