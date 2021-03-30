from griddlers.cells_line import CellsLine
from griddlers.cell_mark import CellMark
from griddlers.cells_section import CellsSection


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


def test_cells_line_sections():
    assert CellsLine.parse_line("X__OOO_X").sections == [
        CellsSection(start=0, end=0, mark=CellMark.CROSSED),
        CellsSection(start=1, end=2, mark=CellMark.EMPTY),
        CellsSection(start=3, end=5, mark=CellMark.FILLED),
        CellsSection(start=6, end=6, mark=CellMark.EMPTY),
        CellsSection(start=7, end=7, mark=CellMark.CROSSED),
    ]


def test_cells_line_sections_after_set():
    cells_line = CellsLine.parse_line("X__OOO_X")
    cells_line[6] = CellMark.FILLED
    assert cells_line.sections == [
        CellsSection(start=0, end=0, mark=CellMark.CROSSED),
        CellsSection(start=1, end=2, mark=CellMark.EMPTY),
        CellsSection(start=3, end=6, mark=CellMark.FILLED),
        CellsSection(start=7, end=7, mark=CellMark.CROSSED),
    ]


def test_cells_line_filled_sections():
    assert CellsLine.parse_line("X_OOXO_X").filled_sections == [
        CellsSection(start=2, end=3, mark=CellMark.FILLED),
        CellsSection(start=5, end=5, mark=CellMark.FILLED),
    ]


def test_cells_line_empty_sections():
    assert CellsLine.parse_line("X__OXO_X").empty_sections == [
        CellsSection(start=1, end=2, mark=CellMark.EMPTY),
        CellsSection(start=6, end=6, mark=CellMark.EMPTY),
    ]


def test_cells_line_contains():
    cells_line = CellsLine.parse_line("___OOO_O")
    assert CellMark.EMPTY in cells_line
    assert CellMark.FILLED in cells_line
    assert CellMark.CROSSED not in cells_line

    cells_line[1] = CellMark.CROSSED

    assert CellMark.CROSSED in cells_line
