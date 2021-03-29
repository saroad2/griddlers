import pytest

from griddlers.cell_mark import CellMark, CellsLine
from griddlers.griddlers_board import GriddlersBoard


def test_griddlers_board_init():
    board = GriddlersBoard(rows=2, columns=3)

    assert str(board) == "___\n___"


def test_griddlers_board_set_cell():
    board = GriddlersBoard(rows=2, columns=3)
    board[0, 1] = CellMark.FILLED

    assert str(board) == "_O_\n___"


def test_griddlers_board_set_row():
    board = GriddlersBoard(rows=2, columns=3)
    board.set_row(0, CellsLine.parse_line("OOX"))

    assert str(board) == "OOX\n___"


def test_griddlers_board_set_column():
    board = GriddlersBoard(rows=2, columns=3)
    board.set_column(0, CellsLine.parse_line("OX"))

    assert str(board) == "O__\nX__"


def test_griddlers_board_get_rows_and_columns():
    board = GriddlersBoard(rows=2, columns=3)
    board[0, 0] = CellMark.FILLED
    board[0, 1] = CellMark.FILLED
    board[1, 0] = CellMark.CROSSED
    board[1, 2] = CellMark.FILLED

    assert str(board) == "OO_\nX_O"

    assert board.get_row(0) == CellsLine.parse_line("OO_")
    assert board.get_row(1) == CellsLine.parse_line("X_O")

    assert board.get_column(0) == CellsLine.parse_line("OX")
    assert board.get_column(1) == CellsLine.parse_line("O_")
    assert board.get_column(2) == CellsLine.parse_line("_O")


def test_griddlers_board_clear():
    board = GriddlersBoard(rows=2, columns=3)
    board[0, 0] = CellMark.FILLED
    board[0, 1] = CellMark.FILLED
    board[1, 0] = CellMark.CROSSED
    board[1, 2] = CellMark.FILLED
    board.clear()

    assert str(board) == "___\n___"


def test_set_minus_1_row():
    board = GriddlersBoard(rows=2, columns=3)
    with pytest.raises(
        ValueError, match="^Row number should be between 0 and 1. Got -1$"
    ):
        board[-1, 1] = CellMark.FILLED


def test_set_too_big_row():
    board = GriddlersBoard(rows=2, columns=3)
    with pytest.raises(
        ValueError, match="^Row number should be between 0 and 1. Got 3$"
    ):
        board[3, 1] = CellMark.FILLED


def test_set_minus_1_column():
    board = GriddlersBoard(rows=2, columns=3)
    with pytest.raises(
        ValueError, match="^Column number should be between 0 and 2. Got -1$"
    ):
        board[1, -1] = CellMark.FILLED


def test_set_too_big_column():
    board = GriddlersBoard(rows=2, columns=3)
    with pytest.raises(
        ValueError, match="^Column number should be between 0 and 2. Got 3$"
    ):
        board[1, 3] = CellMark.FILLED


def test_set_invalid_value():
    board = GriddlersBoard(rows=2, columns=3)
    with pytest.raises(
        ValueError, match="^Can only set marks on board. Got 4$"
    ):
        board[1, 2] = 4
