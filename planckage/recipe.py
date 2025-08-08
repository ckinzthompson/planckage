# # import requests
# # import zipfile
# # import io
# # import os

# import time
# import tomllib

import shutil
import zipfile
from pathlib import Path
from platformdirs import user_data_dir

from . import __data__,__datalist__,__results__,__figures__,__planckage__,__undo__
from . import utils, registry

def cook(recipe_name: str, path: str = './'):
	toplevel = utils.get_toplevel(path)
	if not (toplevel / __planckage__).exists():
		print('Not a planckage repo!')
		return
	
	localregistry = registry.load()
	if not recipe_name in localregistry:
		print('No recipe called "{recipe}" in registry...')
		return
	else:
		## get zip location
		rec = localregistry[recipe_name]
		zip_path = Path(rec['Location']) ## update to handle URLs later....
		if not zip_path.exists():
			print('Cannot find zip file: {zip_path}')
			return
		
		## check if any overwrites will occur
		flag_existing = False
		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			for member in zip_ref.namelist():
				target_path = toplevel / member
				if target_path.exists():
					flag_existing = True
		
		print(f'Cooking recipe: {recipe_name}')
		if flag_existing:
			prompt = input('This will overwrite files. Continue? [Y]es/[N]o? ').lower()
			if not prompt in ['yes','y']:
				print('Canceled.')
				return

		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			zip_ref.extractall(toplevel)
	
	message = f"Successfully cooked recipe: {recipe_name}"
	print(message)
	utils.log(toplevel,message)

def create(recipe_name: str, path: str = './'):
	## check that there's not another already existing
	rn = registry.sanitize(recipe_name)
	
	localregistry = registry.load()
	if rn in localregistry:
		print('That recipe already exists!')
		registry.list(rn)
		return
	
	## assemble files to include
	toplevel = utils.get_toplevel(path).resolve()
	if not (toplevel/__planckage__).exists():
		print('This is not a planckage repo!')
		return
	keep = []
	for obj in toplevel.iterdir():
		if not obj.resolve() in [toplevel/__data__.resolve(),toplevel/__datalist__.resolve(),toplevel/__results__.resolve(),toplevel/__figures__.resolve(),toplevel/__planckage__.resolve()]:
			keep.append(obj.resolve())

	# ## and show them...
	# print(f'== Recipe name: {rn} ==')
	# print('== Putative Contents ==')
	# for obj in keep:
	# 	print(keep.name)
	# print('')

	## prompt for description
	description = input(f'Enter "{rn}" recipe description...\n').replace('\"',"\'")
	# print(f"== Description ==\n{description}\n")

	## zip into temp zip
	zip_path = registry.__userdata__ / f"{rn}.zip"
	with zipfile.ZipFile(zip_path, "w") as zipf:
		for obj in keep:
			zipf.write(obj.resolve(), arcname=obj.name)
	
	registry.backup()
	registry.add(rn,description,zip_path)

def remove(recipe_name: str):
	## check that there's not another already existing
	rn = registry.sanitize(recipe_name)
		
	localregistry = registry.load()
	if not rn in localregistry:
		print(f'Recipe "{rn}" is not in registry')
		return

	registry.backup()
	registry.remove(rn)
	print(f'Removed recipe "{rn}" from registry')



# def list_remote():
# 	try:
# 		registry = toml.load(FILE)
# 		for entry in registry.get("recipes", []):
# 			print(f"- {entry['name']}: {entry['description']}")
# 	except Exception as e:
# 		print(f"❌ Failed to fetch registry: {e}")

# def download(name_or_url: str, toplevel: Path):
# 	recipes_dir = toplevel / "recipes"
# 	recipes_dir.mkdir(exist_ok=True)

# 	# Determine if name_or_url is a URL or a registry name
# 	if name_or_url.startswith("http"):
# 		url = name_or_url
# 	else:
# 		try:
# 			registry = toml.load(FILE)
# 			match = next((r for r in registry.get("recipes", []) if r["name"] == name_or_url), None)
# 			if not match:
# 				print(f"❌ Recipe '{name_or_url}' not found in registry.")
# 				return
# 			url = match["url"]
# 		except Exception as e:
# 			print(f"❌ Failed to fetch registry: {e}")
# 			return

# 	print(f"📦 Downloading from: {url}")
# 	try:
# 		r = requests.get(url)
# 		r.raise_for_status()
# 		z = zipfile.ZipFile(io.BytesIO(r.content))
# 		temp_dir = recipes_dir / "__temp_recipe__"
# 		if temp_dir.exists():
# 			shutil.rmtree(temp_dir)
# 		z.extractall(temp_dir)

# 		# Validate and move
# 		toml_files = list(temp_dir.rglob("recipe.toml"))
# 		if not toml_files:
# 			print("❌ No recipe.toml found in downloaded recipe.")
# 			shutil.rmtree(temp_dir)
# 			return

# 		recipe_folder = toml_files[0].parent
# 		metadata = toml.load(toml_files[0])
# 		final_name = metadata.get("name", recipe_folder.name).replace(" ", "_")
# 		final_path = recipes_dir / final_name

# 		if final_path.exists():
# 			print(f"⚠️ Overwriting existing recipe at {final_path}")
# 			shutil.rmtree(final_path)

# 		shutil.move(str(recipe_folder), str(final_path))
# 		shutil.rmtree(temp_dir)

# 		print(f"✅ Installed recipe: {metadata['name']} -> ./recipes/{final_path.name}")

# 	except Exception as e:
# 		print(f"❌ Failed to download or install recipe: {e}")
