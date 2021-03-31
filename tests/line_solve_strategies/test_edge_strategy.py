from pytest_cases import parametrize_with_cases
from griddlers.cells_line import CellsLine
from griddlers.line_solve_strategies import EdgeStrategy


def case_one_cell_start():
    line = "O______"
    instructions = [3, 2]
    result_line = "OOOX___"

    return line, instructions, result_line


def case_one_cell_start_after_crossed():
    line = "XO______"
    instructions = [3, 2]
    result_line = "XOOOX___"

    return line, instructions, result_line


def case_one_block_start():
    line = "OO_____"
    instructions = [3, 2]
    result_line = "OOOX___"

    return line, instructions, result_line


def case_two_blocks_start_two_filled():
    line = "O___O___"
    instructions = [3, 2]
    result_line = "OOOXOOX_"

    return line, instructions, result_line


def case_two_blocks_start_one_filled():
    line = "O____O__"
    instructions = [3, 2]
    result_line = "OOOX_O__"

    return line, instructions, result_line


def case_one_cell_start_fill_all():
    line = "O___"
    instructions = [4]
    result_line = "OOOO"

    return line, instructions, result_line


def case_three_blocks_start_combined():
    line = "OOXXO_O___"
    instructions = [2, 3]
    result_line = "OOXXOOOX__"

    return line, instructions, result_line


def case_one_cell_end():
    line = "______O"
    instructions = [3, 2]
    result_line = "____XOO"

    return line, instructions, result_line


def case_one_cell_end_before_crossed():
    line = "______OX"
    instructions = [3, 2]
    result_line = "____XOOX"

    return line, instructions, result_line


def case_one_block_end():
    line = "_____OO"
    instructions = [3, 2]
    result_line = "____XOO"

    return line, instructions, result_line


def case_two_blocks_end_two_filled():
    line = "____O__O"
    instructions = [3, 2]
    result_line = "_XOOOXOO"

    return line, instructions, result_line


def case_two_blocks_end_one_filled():
    line = "___O___O"
    instructions = [3, 2]
    result_line = "___O_XOO"

    return line, instructions, result_line


def case_one_cell_end_fill_all():
    line = "___O"
    instructions = [4]
    result_line = "OOOO"

    return line, instructions, result_line


def case_start_and_end():
    line = "O______O"
    instructions = [3, 2]
    result_line = "OOOX_XOO"

    return line, instructions, result_line


@parametrize_with_cases(argnames=["line", "instructions", "result_line"], cases=".")
def test_edge_strategy(line, instructions, result_line):
    edge_strategy = EdgeStrategy()

    input_line = CellsLine.parse_line(line)
    actual_result = edge_strategy.solve(line=input_line, instructions=instructions)
    expected_result = CellsLine.parse_line(result_line)

    assert actual_result == expected_result
    if line != result_line:
        assert actual_result != input_line
