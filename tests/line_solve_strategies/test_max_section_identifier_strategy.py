from pytest_cases import parametrize_with_cases
from griddlers.cells_line import CellsLine
from griddlers.line_solve_strategies import MaxSectionIdentifierStrategy


def case_identify_max_at_start():
    line = "OOO____"
    instructions = [3, 2]
    result_line = "OOOX___"

    return line, instructions, result_line


def case_identify_max_at_middle():
    line = "___OOO____"
    instructions = [3, 2]
    result_line = "__XOOOX___"

    return line, instructions, result_line


def case_identify_max_at_end():
    line = "____OOO"
    instructions = [3, 2]
    result_line = "___XOOO"

    return line, instructions, result_line


def case_identify_second_max_identified():
    line = "__XOOOX__OO___"
    instructions = [1, 3, 2, 1]
    result_line = "__XOOOX_XOOX__"

    return line, instructions, result_line


def case_identify_max_not_identified():
    line = "____OO___"
    instructions = [3, 2]
    result_line = "____OO___"

    return line, instructions, result_line


def case_two_maxes():
    line = "___XOOOX__OOO_____"
    instructions = [3, 3, 2]
    result_line = "___XOOOX_XOOOX____"

    return line, instructions, result_line


def case_completed_line():
    line = "XXXOOOXOOX"
    instructions = [3, 2]
    result_line = "XXXOOOXOOX"

    return line, instructions, result_line


@parametrize_with_cases(argnames=["line", "instructions", "result_line"], cases=".")
def test_max_section_identifier_strategy(line, instructions, result_line):
    max_section_identifier_strategy = MaxSectionIdentifierStrategy()

    input_line = CellsLine.parse_line(line)
    actual_result = max_section_identifier_strategy.solve(
        line=input_line, instructions=instructions
    )
    expected_result = CellsLine.parse_line(result_line)

    assert actual_result == expected_result
    if line != result_line:
        assert actual_result != input_line
