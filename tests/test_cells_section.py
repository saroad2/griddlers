from griddlers.cell_mark import CellMark
from griddlers.cells_section import CellsSection


def test_cell_section_constructor():
    start, end, mark = 4, 6, CellMark.FILLED
    blocked_below, blocked_above = True, False
    section = CellsSection(
        start=start,
        end=end,
        mark=mark,
        blocked_below=blocked_below,
        blocked_above=blocked_above,
    )

    assert section.start == start
    assert section.end == end
    assert section.mark == mark
    assert section.blocked_below is blocked_below
    assert section.blocked_above is blocked_above
    assert section.length == 3


def test_cell_section_one_number():
    n, mark = 4, CellMark.CROSSED
    blocked_below, blocked_above = False, True
    section = CellsSection(
        start=n,
        end=n,
        mark=mark,
        blocked_below=blocked_below,
        blocked_above=blocked_above,
    )

    assert section.start == n
    assert section.end == n
    assert section.mark == mark
    assert section.blocked_below is blocked_below
    assert section.blocked_above is blocked_above
    assert section.length == 1


def test_cell_section_contains():
    start, end, mark = 4, 6, CellMark.FILLED
    blocked_below, blocked_above = False, True
    section = CellsSection(
        start=start,
        end=end,
        mark=mark,
        blocked_below=blocked_below,
        blocked_above=blocked_above,
    )

    for i in range(start, end + 1):
        assert i in section
    assert start - 1 not in section
    assert end + 1 not in section


def test_cell_section_to_list():
    start, end, mark = 4, 6, CellMark.FILLED
    blocked_below, blocked_above = True, False
    section = CellsSection(
        start=start,
        end=end,
        mark=mark,
        blocked_below=blocked_below,
        blocked_above=blocked_above,
    )

    assert list(section) == [4, 5, 6]


def test_cell_section_blocked():
    start, end, mark = 4, 6, CellMark.FILLED
    section = CellsSection(
        start=start, end=end, mark=mark, blocked_below=True, blocked_above=True
    )

    assert section.blocked_below
    assert section.blocked_above
    assert section.blocked


def test_cell_section_blocked_below_only():
    start, end, mark = 4, 6, CellMark.FILLED
    section = CellsSection(
        start=start, end=end, mark=mark, blocked_below=True, blocked_above=False
    )

    assert section.blocked_below
    assert not section.blocked_above
    assert not section.blocked


def test_cell_section_blocked_above_only():
    start, end, mark = 4, 6, CellMark.FILLED
    section = CellsSection(
        start=start, end=end, mark=mark, blocked_below=False, blocked_above=True
    )

    assert not section.blocked_below
    assert section.blocked_above
    assert not section.blocked
