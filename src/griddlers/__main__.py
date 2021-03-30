import click

from griddlers.griddlers_game import GriddlersGame
from griddlers.griddlers_solver import GriddlersSolver


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
    click.echo(game.board_string())


solve_cli()
