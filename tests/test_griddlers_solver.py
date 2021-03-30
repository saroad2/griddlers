from pathlib import Path
import pytest

from griddlers.griddlers_game import GriddlersGame
from griddlers.griddlers_solver import GriddlersSolver

resources_dir = Path(__file__).parent.parent / "resources"
cases = [path for path in resources_dir.iterdir()]


@pytest.mark.parametrize("game_path", cases, ids=lambda gp: gp.stem)
def test_griddlers_solver(game_path):
    game = GriddlersGame.load_from_file(game_path)
    solver = GriddlersSolver()

    solver.solve(game)
    assert game.is_complete, f"Game is not complete:\n{game.board_string()}"
