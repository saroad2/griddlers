from griddlers.cells_line import CellsLine
from griddlers.cell_mark import CellMark


def test_parse_cells_line():
    assert CellsLine.parse_line("X__OOO_X") == CellsLine(
        cells=[
            CellMark.CROSSED,
            CellMark.EMPTY,
            CellMark.EMPTY,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.EMPTY,
            CellMark.CROSSED,
        ]
    )


def test_cells_line_to_str():
    cell_line = CellsLine(
        cells=[
            CellMark.CROSSED,
            CellMark.EMPTY,
            CellMark.EMPTY,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.EMPTY,
            CellMark.CROSSED,
        ]
    )
    assert str(cell_line) == "X__OOO_X"


def test_cells_line_is_not_completed():
    cell_line = CellsLine(
        cells=[
            CellMark.CROSSED,
            CellMark.EMPTY,
            CellMark.EMPTY,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.EMPTY,
            CellMark.CROSSED,
        ]
    )
    assert not cell_line.is_completed


def test_cells_line_is_completed():
    cell_line = CellsLine(
        cells=[
            CellMark.CROSSED,
            CellMark.CROSSED,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.FILLED,
            CellMark.CROSSED,
        ]
    )
    assert cell_line.is_completed


def test_cells_line_get_item():
    cells_line = CellsLine.parse_line("X__OOO_X")
    assert cells_line[0] == CellMark.CROSSED
    assert cells_line[1] == CellMark.EMPTY
    assert cells_line[2] == CellMark.EMPTY
    assert cells_line[3] == CellMark.FILLED
    assert cells_line[4] == CellMark.FILLED
    assert cells_line[5] == CellMark.FILLED
    assert cells_line[6] == CellMark.EMPTY
    assert cells_line[7] == CellMark.CROSSED


def test_cells_line_set_item():
    cells_line = CellsLine.parse_line("X__OOO_X")
    cells_line[1] = CellMark.CROSSED
    assert cells_line == CellsLine.parse_line("XX_OOO_X")


def test_cells_line_inverse():
    cells_line = CellsLine.parse_line("X__OOO_X")
    assert cells_line.inverse() == CellsLine.parse_line("X_OOO__X")


def test_cells_line_length():
    assert len(CellsLine.parse_line("X__OOO_X")) == 8
    assert len(CellsLine.parse_line("XX_X")) == 4
    assert len(CellsLine.parse_line("O")) == 1
    assert len(CellsLine.parse_line("")) == 0


def test_cells_line_convert_to_list():
    assert list(CellsLine.parse_line("X__OOO_X")) == [
        CellMark.CROSSED,
        CellMark.EMPTY,
        CellMark.EMPTY,
        CellMark.FILLED,
        CellMark.FILLED,
        CellMark.FILLED,
        CellMark.EMPTY,
        CellMark.CROSSED
    ]
