import time
import shutil
import tomllib
from pathlib import Path

from . import __version__
from . import __log__, __planckage__, __results__, __figures__, __data__
from . import utils

def init(project_name: str = "./"):
	"""
	Creates a new project - files and folders 
	"""

	project_path = Path(project_name)
	if (project_path / __planckage__).exists():
		raise FileExistsError(f"'{project_name}' is already a planckage project!")
	
	project_path.mkdir()
	(project_path / __planckage__).mkdir()
	(project_path / __data__).mkdir()
	(project_path / __results__).mkdir()
	(project_path / __figures__).mkdir()

	(project_path / __log__).touch()
	with (project_path / __log__).open("w") as f:
		f.write(f"Created new planckage project at: {time.ctime()}\n")# Location: {project_path.resolve()}\n") ## Location is a bit invasive

def clone(source: str, destination: str = "./"):
	"""
	Copy planckage repo at source to destination
	"""

	from urllib.parse import urlparse
	loc = urlparse(source)
	if loc.scheme in ['http', 'https', 'ftp'] and loc.netloc != '':
		raise Exception("Cloning a URL is not supported yet. Check back later!")

	path_src = Path(source).resolve()
	if not path_src.is_dir() or not (path_src / '.planckage').exists():
		raise Exception('Source is not a planckage repo')
	print(path_src.name)

	path_dst = Path(destination).resolve()

	if not path_dst.exists():
		path_dst.mkdir()
	elif path_dst.is_file():
		raise Exception('Destination is a file')
	
	if path_dst.is_dir():
		if (path_dst / ".planckage").exists():
			raise Exception('Destination is already a planckage repo')
		
	shutil.copytree(path_src, path_dst, dirs_exist_ok=True)

	## This will make the lock on somone else's disappear.... so how could someone check?
	## Need to think more abou this....
	# unlock(path_dst)	
	# with (path_dst / __log__).open('a') as f:
	# 	f.write(f'\nCloned from {path_src}')

# def unlock(project_path: Path = './'):
# 	if (project_path / __planckage__ / 'lock.toml').exists():
# 		(project_path / __planckage__ / 'lock.toml').unlink()

def lock(project_path: Path = './'):
	hash_log, hash_all = utils.hash_planckage(project_path)
	with open(project_path / __log__, 'r') as f:
		create_time = f.readline()
		ind = create_time.index(":")
		create_time = create_time[ind+1:].strip()

	with (project_path / __planckage__ / "lock.toml").open('w') as f:
		f.write('# Planckage lock file\n')
		f.write(f'planckage_version = \"{__version__}\"\n')
		f.write(f'create_time = \"{create_time}\"\n\n')
		lock_time = time.ctime()
		f.write(f'lock_time = \"{lock_time}\"\n')

		f.write(f'[hashes]\n')
		f.write(f'log = \"{hash_log}\"\n')
		f.write(f'allfiles = \"{hash_all}\"\n\n')

	print('== Locked ==')
	print(f'Locked at:     {lock_time}')
	print(f'Lock hash:     {hash_all}')

def check(project_path: Path = './'):
	hash_log, hash_all = utils.hash_planckage(project_path)

	lock_path = project_path / __planckage__ / "lock.toml"
	if not lock_path.exists():
		print(f'No lockfile at {lock_path.resolve()}')
		print(f'Current hash: {hash_all}')
		return
	lock = tomllib.load(lock_path.open('rb'))
	
	try:
		assert lock['hashes']['log'] == hash_log
		assert lock['hashes']['allfiles'] == hash_all
		print('== Lock has not been tampered with ==')
	except:
		print('== Lock has been tampered with ==')

	print(f'Created:      {lock['create_time']}')
	print(f'Locked:       {lock['lock_time']}')
	print(f'Lock hash:    {lock['hashes']['allfiles']}')
	print(f'Current hash: {hash_all}')