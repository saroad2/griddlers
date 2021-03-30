from griddlers.cell_mark import CellMark
from griddlers.cells_section import CellsSection


def test_cell_section_constructor():
    start, end, mark = 4, 6, CellMark.FILLED
    section = CellsSection(start=start, end=end, mark=mark)

    assert section.start == start
    assert section.end == end
    assert section.mark == mark
    assert section.length == 3


def test_cell_section_one_number():
    n, mark = 4, CellMark.CROSSED
    section = CellsSection(start=n, end=n, mark=mark)

    assert section.start == n
    assert section.end == n
    assert section.mark == mark
    assert section.length == 1


def test_cell_section_contains():
    start, end, mark = 4, 6, CellMark.FILLED
    section = CellsSection(start=start, end=end, mark=mark)

    for i in range(start, end + 1):
        assert i in section
    assert start - 1 not in section
    assert end + 1 not in section


def test_cell_section_to_list():
    start, end, mark = 4, 6, CellMark.FILLED
    section = CellsSection(start=start, end=end, mark=mark)

    assert list(section) == [4, 5, 6]

