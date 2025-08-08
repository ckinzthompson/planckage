import hashlib
from pathlib import Path

from . import __log__, __planckage__, __results__, __figures__, __data__

def hashfile(fn: Path):
	bf = open(fn,'rb').read()
	hash = hashlib.sha256(bf).hexdigest()
	return hash

def hash_planckage(project_path: Path):
	hash_log =  hashfile(project_path / __log__)
	hash_all = hashlib.sha256()
	for fn in project_path.rglob('*'):
		if fn == project_path / __planckage__ / 'lock.toml':
			continue
		if fn.is_dir():
			continue
		hash = hashfile(fn)
		hash_all.update(bytes.fromhex(hash))
	hash_all = hash_all.hexdigest()
	return hash_log, hash_all

def log(project_path: Path, message: str):
	suffix = '\n' if not message.endswith('\n') else ''
	(project_path / __log__).open('a').write(message+suffix)

def get_toplevel(cwd: str):
	## get top-level path
	toplevel = Path(cwd)
	if not (toplevel / '.planckage').exists():
		for parent in Path(toplevel).resolve().parents:
			if (parent / '.planckage').exists():
				toplevel = parent
				break
	return toplevel