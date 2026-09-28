import hashlib
import mimetypes
import os
import re
import shutil
from pathlib import Path, PurePosixPath, PureWindowsPath
import tempfile
import unicodedata


def _safe_segment(value):
	text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii").lower()
	segment = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
	return segment[:40].rstrip("-") or "item"


def _safe_filename(value):
	name = PureWindowsPath(str(value)).name
	name = unicodedata.normalize("NFKC", name)
	name = re.sub(r'[\x00-\x1f<>:"/\\|?*]', "_", name).strip(" .")
	return (name or "file")[:120]


def _original_filename(value):
	name = PureWindowsPath(str(value)).name
	if not name or any(ord(char) < 32 for char in name):
		raise ValueError("original filename is empty or contains control characters")
	return name


def safe_vault_path(root, relative_path):
	if not isinstance(relative_path, str) or not relative_path.strip() or "\\" in relative_path:
		raise ValueError("vault paths must be non-empty POSIX-relative paths")
	if PureWindowsPath(relative_path).drive or PureWindowsPath(relative_path).is_absolute():
		raise ValueError("absolute paths are not allowed")
	if relative_path.startswith("/"):
		raise ValueError("absolute paths are not allowed")
	parts = relative_path.split("/")
	if any(part in ("", ".", "..") for part in parts):
		raise ValueError("vault paths cannot contain empty, current, or parent segments")
	base = Path(root).resolve()
	target = (base / Path(*PurePosixPath(relative_path).parts)).resolve()
	if not target.is_relative_to(base):
		raise ValueError("vault path escapes the configured root")
	return target


def sha256_file(path):
	digest = hashlib.sha256()
	with Path(path).open("rb") as file:
		for chunk in iter(lambda: file.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _store_stream(stream, root, folders, original_filename):
	root = Path(root)
	root.mkdir(parents=True, exist_ok=True)
	root = root.resolve()
	folder_parts = tuple(_safe_segment(part) for part in folders)
	if not folder_parts:
		raise ValueError("a course or collection folder is required")
	filename = _original_filename(original_filename)
	sha = hashlib.sha256()
	byte_size = 0
	with tempfile.TemporaryFile(dir=root) as staged:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			sha.update(chunk)
			byte_size += len(chunk)
			staged.write(chunk)
		digest = sha.hexdigest()
		safe_name = _safe_filename(filename)
		relative = PurePosixPath(*folder_parts, f"{digest}-{safe_name}").as_posix()
		target = safe_vault_path(root, relative)
		target.parent.mkdir(parents=True, exist_ok=True)
		staged.seek(0)
		created = False
		try:
			with target.open("xb") as output:
				created = True
				shutil.copyfileobj(staged, output, length=1024 * 1024)
		except FileExistsError:
			if sha256_file(target) != digest:
				raise OSError("a different file already occupies the content-addressed vault path")
		except BaseException:
			if created:
				target.unlink(missing_ok=True)
			raise
		return {
			"original_filename": filename,
			"vault_relative_path": relative,
			"sha256": digest,
			"byte_size": byte_size,
			"content_type": mimetypes.guess_type(safe_name)[0] or "application/octet-stream",
		}


def store_local_file(source_path, root, folders, original_filename=None):
	source = Path(source_path).resolve(strict=True)
	if not source.is_file():
		raise ValueError("source must be a regular file")
	with source.open("rb") as stream:
		return _store_stream(stream, root, folders, original_filename or source.name)


def store_bytes(content, root, folders, original_filename):
	from io import BytesIO

	return _store_stream(BytesIO(content), root, folders, original_filename)


def vault_root():
	import frappe

	configured = frappe.conf.get("studies_hub_vault_root") or os.environ.get("STUDIES_HUB_VAULT_ROOT")
	if not configured:
		raise RuntimeError("Set studies_hub_vault_root or STUDIES_HUB_VAULT_ROOT to a visible local vault directory.")
	return Path(configured).resolve()


def open_vault_file(relative_path):
	path = safe_vault_path(vault_root(), relative_path)
	if not path.is_file():
		raise FileNotFoundError("registered local artifact is missing")
	return path
