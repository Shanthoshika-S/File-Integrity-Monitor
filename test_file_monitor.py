
import hashlib
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.file_monitor import calculate_file_hash, check_integrity


class TestFileIntegrityMonitor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.test_folder = Path(self.temp_dir.name)
        self.monitored_folder = self.test_folder / "monitored_files"
        self.monitored_folder.mkdir()

        self.baseline_file = self.test_folder / "baseline.json"

        self.folder_patch = patch(
            "src.file_monitor.MONITORED_FOLDER",
            self.monitored_folder
        )
        self.baseline_patch = patch(
            "src.file_monitor.BASELINE_FILE",
            self.baseline_file
        )

        self.folder_patch.start()
        self.baseline_patch.start()

    def tearDown(self):
        self.folder_patch.stop()
        self.baseline_patch.stop()
        self.temp_dir.cleanup()

    def save_baseline(self, data):
        with self.baseline_file.open("w", encoding="utf-8") as file:
            json.dump(data, file)

    def run_integrity_check(self):
        output = StringIO()

        with redirect_stdout(output):
            check_integrity()

        return output.getvalue()

    def test_hash_calculation(self):
        test_file = self.monitored_folder / "test.txt"
        test_file.write_text("hello", encoding="utf-8")

        expected_hash = hashlib.sha256(b"hello").hexdigest()

        self.assertEqual(
            calculate_file_hash(test_file),
            expected_hash
        )

    def test_modified_file_detection(self):
        test_file = self.monitored_folder / "config.txt"
        test_file.write_text("new content", encoding="utf-8")

        self.save_baseline({
            "config.txt": hashlib.sha256(b"old content").hexdigest()
        })

        output = self.run_integrity_check()

        self.assertIn("[MODIFIED] config.txt", output)

    def test_deleted_file_detection(self):
        self.save_baseline({
            "users.txt": hashlib.sha256(b"username=admin").hexdigest()
        })

        output = self.run_integrity_check()

        self.assertIn("[DELETED] users.txt", output)

    def test_new_file_detection(self):
        test_file = self.monitored_folder / "backup.txt"
        test_file.write_text("backup=enabled", encoding="utf-8")

        self.save_baseline({})

        output = self.run_integrity_check()

        self.assertIn("[NEW] backup.txt", output)


if __name__ == "__main__":
    unittest.main()
