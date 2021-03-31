import click

from griddlers.cell_mark import CellMark
from griddlers.griddlers_game import GriddlersGame
from griddlers.griddlers_solver import GriddlersSolver


def color_fill(char):
    if char == CellMark.FILLED.value:
        return click.style(char, fg="yellow")
    return char


@click.command("solve")
@click.argument("game_file", type=click.Path(dir_okay=False, exists=True))
def solve_cli(game_file):
    game = GriddlersGame.load_from_file(game_file)
    solver = GriddlersSolver()

    solver.solve(game)
    if game.is_complete:
        click.echo(click.style("Finished game!", fg="green"))
    else:
        click.echo(click.style("Game lost...", fg="red"))
    for line in game.board_string().split("\n"):
        click.echo(''.join(color_fill(char) for char in line))


solve_cli()
