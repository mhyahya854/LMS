import json
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]


class DocTypeMetadataTests(unittest.TestCase):
	def test_standard_doctype_json_has_unique_and_complete_field_order(self):
		paths = sorted((APP_ROOT / "academic" / "doctype").glob("*/*.json"))
		self.assertEqual(len(paths), 6)
		metadata = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
		names = {doctype["name"] for doctype in metadata}
		for path in paths:
			with self.subTest(doctype=path.parent.name):
				meta = json.loads(path.read_text(encoding="utf-8"))
				field_names = [field["fieldname"] for field in meta["fields"]]
				self.assertEqual(len(field_names), len(set(field_names)))
				self.assertEqual(set(field_names), set(meta["field_order"]))
				self.assertEqual(meta["doctype"], "DocType")
				self.assertEqual(meta["module"], "Academic")
				self.assertTrue(meta["autoname"].startswith("UUID"))
				for field in meta["fields"]:
					if field["fieldtype"] == "Link":
						self.assertIn(field["options"], names)


if __name__ == "__main__":
	unittest.main()
