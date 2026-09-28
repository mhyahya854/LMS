import tempfile
import unittest
from pathlib import Path

from studies_hub.vault.storage import safe_vault_path, sha256_file, store_bytes, store_local_file


class VaultStorageTests(unittest.TestCase):
	def setUp(self):
		self.temp = tempfile.TemporaryDirectory()
		self.root = Path(self.temp.name) / "Academic Vault"

	def tearDown(self):
		self.temp.cleanup()

	def test_safe_path_rejects_traversal_and_absolute_paths(self):
		for path in ("../outside.txt", "course/../../outside.txt", "/etc/passwd", "C:/private/file.txt", "course\\file.txt"):
			with self.subTest(path=path), self.assertRaises(ValueError):
				safe_vault_path(self.root, path)

	def test_safe_path_rejects_symlink_escape(self):
		self.root.mkdir(parents=True)
		outside = Path(self.temp.name) / "outside"
		outside.mkdir()
		try:
			(self.root / "escape").symlink_to(outside, target_is_directory=True)
		except (OSError, NotImplementedError):
			self.skipTest("This Windows volume does not allow unprivileged symlink creation")
		with self.assertRaises(ValueError):
			safe_vault_path(self.root, "escape/file.txt")

	def test_content_addressing_deduplicates_identical_file_and_preserves_name(self):
		first = store_bytes(b"synthetic lecture material", self.root, ("Test Data", "Computer Systems", "Lecture 01"), "slides.txt")
		second = store_bytes(b"synthetic lecture material", self.root, ("Test Data", "Computer Systems", "Lecture 01"), "slides.txt")
		self.assertEqual(first["vault_relative_path"], second["vault_relative_path"])
		self.assertEqual(first["original_filename"], "slides.txt")
		self.assertEqual(first["sha256"], sha256_file(safe_vault_path(self.root, first["vault_relative_path"])))

	def test_same_filename_with_different_contents_never_overwrites(self):
		first = store_bytes(b"version one", self.root, ("Test Data", "Computer Systems"), "notes.txt")
		second = store_bytes(b"version two", self.root, ("Test Data", "Computer Systems"), "notes.txt")
		self.assertNotEqual(first["vault_relative_path"], second["vault_relative_path"])
		self.assertEqual(first["original_filename"], second["original_filename"])
		self.assertEqual(safe_vault_path(self.root, first["vault_relative_path"]).read_bytes(), b"version one")
		self.assertEqual(safe_vault_path(self.root, second["vault_relative_path"]).read_bytes(), b"version two")

	def test_local_file_import_streams_into_user_visible_vault(self):
		source = Path(self.temp.name) / "original.txt"
		source.write_text("offline copy", encoding="utf-8")
		stored = store_local_file(source, self.root, ("Computer Systems", "Resources"))
		self.assertEqual(stored["original_filename"], "original.txt")
		self.assertEqual(safe_vault_path(self.root, stored["vault_relative_path"]).read_text(encoding="utf-8"), "offline copy")


if __name__ == "__main__":
	unittest.main()
