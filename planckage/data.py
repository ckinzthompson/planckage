import shutil
from pathlib import Path
from typing import List

from . import __data__,__datalist__, __undo__
from .utils import log

def undo(project_path: Path = './'):
	src = project_path / __undo__ / __datalist__.name
	if src.exists():
		shutil.move(src, project_path / __datalist__)

def readlist(project_path: Path = './') -> List[Path]:
	"""
	Parse entries in ./data.txt
	Returns a list of good entries, and a list of bad entries
	"""
	if not (project_path / __datalist__).exists():
		raise FileNotFoundError(f"Missing {(project_path / __datalist__).resolve()}")
	
	good_files: List[Path] = []
	with open(project_path / __datalist__,"r") as f:
		for line in f:
			candidate = line.strip()
			if "#" in candidate:
				candidate = candidate[:candidate.index("#")]
			candidate = Path(candidate.strip()).resolve()
			if candidate.is_file():
				good_files.append(candidate)
			# else:
			# 	bad_files.append(candidate)
	return good_files

def check(project_path: Path = './'):
	"""
	Comment out bad entries in ./data.txt
	"""
	log(project_path, "## Data Check")
	keep = ''
	with (project_path / __datalist__).open('r') as f:
		for line in f:
			candidate = line.strip()
			if "#" in candidate:
				candidate = candidate[:candidate.index("#")].strip()

			if candidate == '' or candidate is None:
				keep += line
				continue
			else:
				candidate = Path(candidate).resolve()
				if candidate.exists():
					keep += line
				else:
					keep += f"# {line}"
	
	shutil.move(project_path / __datalist__, project_path / __undo__ / __datalist__.name)
	(project_path / __datalist__).open('w').write(keep)
	log(project_path, f'Removed bad entries from {project_path / __datalist__}\n')
	
def localcopy(project_path: Path = './'):
	log(project_path, f'## Local Copy')
	good = readlist(project_path)

	## copy good data
	for path in good:
		if path.is_file():
			if path.exists():
				path.unlink()
			shutil.copy2(path, project_path / __data__ / path.name)
			log(project_path, f'Copied: {path} -> {project_path / __data__ / path.name}')
		elif path.is_dir():
			shutil.copytree(path, project_path / __data__ / path.name,  dirs_exist_ok=True)
			log(project_path, f'Copied: {path} -> {project_path / __data__ / path.name}')
	
	## update data_list
	shutil.move(project_path / __datalist__, project_path / __undo__ / __datalist__.name) ## save the current 
	with (project_path / __datalist__).open('w') as f:
		f.write("## Generated from localcopy action\n")
		f.write("## Enter the path(s) to your data file(s) below\n")
		for p in (project_path / __data__).iterdir():
			if not p == project_path / __datalist__:
				f.write(f"{p.resolve()}\n")
	log(project_path, f'Auto-generated: {project_path / __datalist__}\n')

def add(patterns: List[str], project_path: Path = './'):
	"""
	Takes file(s) and adds them to ./data.txt if not already there
	"""
	log(project_path, '## Adding Data')

	all_matched = []
	for pattern in patterns:

		## Get potential candidates for new data to add
		if any(char in pattern for char in "*?[]"):
			matched = list(Path().glob(pattern))
		else:
			matched = [Path(pattern),]
		matched = [m.resolve() for m in matched]
		matched = [m for m in matched if m.exists()]
		all_matched = all_matched + matched

	## Make sure there's a fresh new line
	if open(project_path / __datalist__, "rb").read()[-1:] != b'\n':
		open(project_path / __datalist__, "a").write('\n')

	## Add good files 
	count = 0
	good = readlist(project_path)

	with (project_path / __datalist__).open('a') as f:
		for match in all_matched:
			if not match in good:
				f.write(f"{match}\n")
				count += 1
	log(project_path, f"Added {count}/{len(all_matched)} new data to {project_path / __datalist__}\n")

	check(project_path)

def clean(project_path: Path = './', prompt: bool = True):
	log(project_path, '## Cleaning Data')
	good = readlist(project_path)
	
	remove_list = []
	for p in (project_path / __data__).iterdir():
		if p == project_path / __datalist__:
			continue
		if not p.resolve() in good:
			remove_list.append(p.resolve())
	
	if prompt:
		print('Are you sure you want to remove the following?'+ ''.join(["\n\t"+str(r) for r in remove_list]))
		answer = input('[y/N]?').strip().lower()
		log(project_path, f'Prompt response: {answer}')
	else:
		answer = 'y'
		log(project_path, 'No prompt')

	if answer in ['y','yes']:
		for path in remove_list:
			if path.is_dir():
				shutil.rmtree(path)
			else:
				path.unlink()
		log(project_path, f'Removed {len(remove_list)} Files')
	else:
		log(project_path, 'Did not remove anything')
	check(project_path)

def convert2rel(project_path: Path = './'):
	"""
	Turn active entries in ./data.txt from path to relative path
	"""
	log(project_path, "## Data transform: path to relative path")
	keep = ''
	with (project_path / __datalist__).open('r') as f:
		for line in f:
			candidate = line.strip()
			if "#" in candidate:
				candidate = candidate[:candidate.index("#")].strip()
			if candidate == '' or candidate is None:
				keep += line
				continue
			else:
				candidate = Path(candidate).resolve()
				if candidate.exists():
					keep += candidate.relative_to(candidate.parents[1])
				else:
					keep += f"# {line}"
	shutil.move(project_path / __datalist__, project_path / __undo__ / __datalist__.name)
	(project_path / __datalist__).open('w').write(keep)
	log(project_path, f'Converted to relative path: {project_path / __datalist__}\n')

def convert2abs(project_path: Path = './'):
	"""
	Turn active entries in ./data.txt from path to absolute path
	"""
	log(project_path, "## Data transform: path to absolute path")
	keep = ''
	with (project_path / __datalist__).open('r') as f:
		for line in f:
			candidate = line.strip()
			if "#" in candidate:
				candidate = candidate[:candidate.index("#")].strip()
			if candidate == '' or candidate is None:
				keep += line
				continue
			else:
				candidate = Path(candidate).resolve()
				if candidate.exists():
					keep += candidate.resolve()
				else:
					keep += f"# {line}"
	shutil.move(project_path / __datalist__, project_path / __undo__ / __datalist__.name)
	(project_path / __datalist__).open('w').write(keep)
	log(project_path, f'Converted to absolute path: {project_path / __datalist__}\n')

def list(project_path: Path = './'):
	good = readlist(project_path)
	print('Good files in data list'+ ''.join(["\n\t"+str(r) for r in good]))