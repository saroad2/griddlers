from pytest_cases import parametrize_with_cases
from griddlers.cells_line import CellsLine
from griddlers.line_solve_strategies import GapsFillerStrategy


def case_fill_first_gap():
    line = "__X________"
    instructions = [3, 2]
    result_line = "XXX________"

    return line, instructions, result_line


def case_fill_last_gap():
    line = "________X__"
    instructions = [2, 3]
    result_line = "________XXX"

    return line, instructions, result_line


def case_fill_min_gap():
    line = "___X_X______"
    instructions = [3, 2]
    result_line = "___XXX______"

    return line, instructions, result_line


def case_not_fill_min_gap_not_blocked():
    line = "___X_OX______"
    instructions = [3, 2]
    result_line = "___X_OX______"

    return line, instructions, result_line


def case_not_fill_first_gap():
    line = "__X_X_____"
    instructions = [2, 1, 3]
    result_line = "__X_X_____"

    return line, instructions, result_line


def case_first_is_known():
    line = "XXOOX__X____X__"
    instructions = [2, 3, 1]
    result_line = "XXOOXXXX____X__"

    return line, instructions, result_line


def case_last_is_known():
    line = "__X____X__XOOXX"
    instructions = [1, 3, 2]
    result_line = "__X____XXXXOOXX"

    return line, instructions, result_line


def case_extend_first_filled_section():
    line = "_O_________"
    instructions = [4, 2]
    result_line = "_OOO_______"

    return line, instructions, result_line


def case_extend_second_filled_section():
    line = "XOOX__O______"
    instructions = [2, 4, 2]
    result_line = "XOOX__OO_____"

    return line, instructions, result_line


def case_extend_last_filled_section():
    line = "_________O_"
    instructions = [2, 4]
    result_line = "_______OOO_"

    return line, instructions, result_line


def case_extend_first_filled_block_backwards():
    line = "__OX_________"
    instructions = [2, 4]
    result_line = "XOOX_________"

    return line, instructions, result_line


def case_extend_second_filled_block_backwards():
    line = "XOOOX__OX_________"
    instructions = [3, 2, 4]
    result_line = "XOOOXXOOX_________"

    return line, instructions, result_line


def case_second_semi_open_section():
    line = "_____OOOX_____"
    instructions = [2, 3, 2]
    result_line = "_____OOOX_____"

    return line, instructions, result_line


@parametrize_with_cases(argnames=["line", "instructions", "result_line"], cases=".")
def test_gaps_filler_strategy(line, instructions, result_line):
    gaps_filler_strategy = GapsFillerStrategy()

    input_line = CellsLine.parse_line(line)
    actual_result = gaps_filler_strategy.solve(
        line=input_line, instructions=instructions
    )
    expected_result = CellsLine.parse_line(result_line)

    assert actual_result == expected_result
    if line != result_line:
        assert actual_result != input_line
