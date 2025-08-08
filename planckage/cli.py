import typer
from . import core, data, utils, recipe, registry
from typing import List
from pathlib import Path

toplevel = utils.get_toplevel('./')

## Setup
app = typer.Typer(help="Planckage: a tool for managing scientific data analysis")#,no_args_is_help=True)
app_data = typer.Typer(help="-> Data-related routines")
app_recipe = typer.Typer(help="-> Recipe-related routines")

## Core
@app.command(help="Make a new planckage repo")
def init(project_name: str = typer.Argument('./', help="Folder name to initialize in")):
	typer.echo(f"Creating new planckage folder: {project_name}")
	core.init(project_name)

@app.command(help="Clone a planckage repo")
def clone(source: str = typer.Argument('./', help="Original planckage repo location"), destination: str = typer.Argument('./', help="Place to put folder containing repo copy")):
	core.clone(source,destination)
	typer.echo(f"Cloning: {source} -> {destination}")

@app.command(help="Create lock file")
def lock():
	core.lock(toplevel)

@app.command(help="Remove lock file")
def unlock():
	core.unlock(toplevel)
	typer.echo(f"Unlocked")

@app.command(help="Check lock file")
def check():
	core.check(toplevel)

## Data
@app_data.command(help="Add new file(s)/folders(s) to ./data.txt")
def add(pattern: List[str]):
	typer.echo(f"Adding File(s)/Folder(s): {pattern}")
	data.add(pattern,toplevel)

@app_data.command(help="Copy ./data.txt entries to ./data")
def copy():
	typer.echo(f"Copying Data to Local Folder")
	data.localcopy(toplevel)

@app_data.command(help='Comment out non-existing ./data.txt entries')
def check():
	typer.echo(f"Checking datalist")
	data.check(toplevel)

@app_data.command(help='Replace ./data.txt with the previous version')
def undo():
	typer.echo(f"Undo datalist edit")
	data.undo(toplevel)

@app_data.command(help='Remove files from ./data that are missing or are non-active entries in ./data.txt')
def clean():
	typer.echo(f"Cleaning local data")
	data.clean(toplevel)

@app_data.command(help='Convert ./data.txt to absolute paths')
def convert2abs():
	typer.echo(f"Converting ./data.txt to absolute paths")
	data.convert2abs(toplevel)

@app_data.command(help='Convert ./data.txt to relative paths')
def convert2rel():
	typer.echo(f"Converting ./data.txt to relative paths")
	data.convert2rel(toplevel)

@app_data.command(help='List data files')
def list():
	data.list(toplevel)

## Recipes
@app_recipe.command(help="Remove everything related to recipes")
def clean():
	registry.clean()
	registry.touch()

@app_recipe.command(help="Remove all recipes from the registry")
def clear():
	prompt = input('Are you sure you want to clear the entire registry?[Y]es/[N]o? ').lower()
	if prompt in ['yes','y']:
		registry.backup()
		registry.clear()
	else:
		print('Canceled.')
		return

@app_recipe.command(help="Execute recipe in current repo")
def cook(recipe_name: str):
	recipe.cook(recipe_name, toplevel)

@app_recipe.command(help="Register the current repo as a recipe")
def create(recipe_name: str):
	recipe.create(recipe_name, toplevel)

@app_recipe.command(help="Say hello")
def hello():
	print('Hello Kitty. Hello!')

@app_recipe.command(help="List all recipes in the registry")
def list():
	registry.list(None)

@app_recipe.command(help="Remove recipe (and files) from registry")
def remove(recipe_name: str):
	recipe.remove(recipe_name)

@app_recipe.command(help="Replace registry with the previous version")
def undo():
	registry.undo()


## Sub-apps
app.add_typer(app_data, name="data")
app.add_typer(app_recipe, name="recipe")

if __name__ == "__main__":
	app()