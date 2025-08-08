import time
import shutil
import tomllib
import zipfile
import tempfile	
from pathlib import Path
from platformdirs import user_data_dir
from . import utils

__userdata__ = Path(user_data_dir(appname='planckage',))
__localreg__ = __userdata__ / 'recipes.toml'
__undoreg__ = __userdata__ / 'recipes.toml.undo'

#### REGISTRY - entries should look like this....
''' 
[<name>]
hash = sha256 of zip at location
created = f"{time.ctime()}"
description = "<string>"
location = "<url or path -- zipfile>"
'''

def touch():
	if not __userdata__.exists():
		print(f'Making user directory: {__userdata__}')
		__userdata__.mkdir()
	__localreg__.touch()

def clear():
	__localreg__.unlink() ## remove registry
	touch() ## make new registry
	print("Cleared Registry")

def load():
	if not __localreg__.exists():
		touch()
	registry = tomllib.load(__localreg__.open('rb'))
	return registry

def list(recipename = None):
	localregistry = load()
	if not localregistry:
		print("Registry is empty...")
		return

	entries = []
	if recipename == None:
		print("\n======== Registry ========\n")
		entries = [entry for entry in localregistry]
	elif recipename in localregistry:
		entries = [recipename,]
	else:
		print(f'Recipe "{recipename}" not in registry...')
		return
	
	for entry in entries:
		print(f"{entry}")
		for key in localregistry[entry]:
			print(f'\t{key.title()}: {localregistry[entry][key]}')
		print('')

	if recipename == None:
		print("==========================")

def fake():
	print('Making fake registry for debugging purposes')
	name = "my_recipe1"
	clear()	
	with tempfile.TemporaryDirectory() as temp_dir:
		hello_path = Path(temp_dir) / 'hello.py'
		with open(hello_path,'w') as f:
			f.write('print("Hello Kitty. Hello!")\n')
		zip_path =__userdata__ / f"{name}.zip"
		with zipfile.ZipFile(zip_path, "w") as zipf:
			zipf.write(hello_path, arcname="hello.py")
	add(name, "It's just a fake recipe",zip_path)
	print('Made fake registry')

def sanitize(recipe_name: str) -> str:
	return recipe_name.strip().replace('\n','').replace(' ','')

def add(name: str, description: str, location: str):
	created = time.ctime()
	hash = utils.hashfile(location)
	with __localreg__.open('a') as f:
		f.write(f'[{name}]\nCreated = "{created}"\nDescription = "{description}"\nLocation = "{location}"\nHash = "{hash}"\n\n')

def remove(name: str):
	keep = ''
	with __localreg__.open('r') as f:
		for line in f:
			if line == f'[{name}]\n':
				created = f.readline()
				description = f.readline()
				location = f.readline()
				hash = f.readline()
				f.readline() ## blank...
				# Path(location).resolve().unlink() ## don't do this for now
			else:
				keep += line
	__localreg__.unlink() ## remove the old
	with __localreg__.open('w') as f: ## write the new
		f.write(keep)

def backup():
	shutil.copy(__localreg__,__undoreg__)
	
def undo():
	if __undoreg__.exists():
		shutil.copy(__undoreg__, __localreg__)

def clean():
	for fn in __userdata__.glob('*.zip'):
		fn.unlink()
	__localreg__.unlink()
	__undoreg__.unlink()