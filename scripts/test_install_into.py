"""Exercise install_into from scripts/install-deps.sh with local fixtures only."""

import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "install-deps.sh"


def find_bash():
    """Return a usable bash, or None. On Windows, prefer Git Bash over the WSL launcher."""
    if os.name != "nt":
        return shutil.which("bash")
    candidates = []
    for var in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        base = os.environ.get(var)
        if base:
            candidates.append(pathlib.Path(base) / "Git" / "bin" / "bash.exe")
            candidates.append(pathlib.Path(base) / "Programs" / "Git" / "bin" / "bash.exe")
    git = shutil.which("git")
    if git:
        candidates.append(pathlib.Path(git).resolve().parent.parent / "bin" / "bash.exe")
    for path in candidates:
        if path.is_file():
            return str(path)
    found = shutil.which("bash")
    if found:
        low = found.lower()
        # Skip the WSL launcher (System32 / WindowsApps).
        if "\system32\\" not in low and "windowsapps" not in low:
            return found
    return None


BASH = find_bash()
MARKER = ".copy-studio-managed"


def run_install_into(src, dest):
    """Source the installer (which installs nothing) and call install_into."""
    env = dict(
        os.environ,
        INSTALLER=SCRIPT.as_posix(),
        SRC=pathlib.Path(src).as_posix(),
        DEST=pathlib.Path(dest).as_posix(),
    )
    return subprocess.run(
        [BASH, "-c", 'source "$INSTALLER" && install_into "$SRC" "$DEST"'],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


@unittest.skipUnless(BASH, "no usable bash found (Git Bash on Windows, or bash on PATH)")
class InstallIntoTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = pathlib.Path(tmp.name)
        self.src = self.root / "src"
        self.src.mkdir()
        (self.src / "SKILL.md").write_text("new skill\n", encoding="utf-8")
        (self.src / "sub").mkdir()
        (self.src / "sub" / "note.txt").write_text("nested\n", encoding="utf-8")
        self.dest = self.root / "dest"

    def backups(self):
        return sorted(self.root.glob("dest.bak-*"))

    def test_new_install_copies_files_and_marks_managed(self):
        result = run_install_into(self.src, self.dest)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.dest / "SKILL.md").read_text(encoding="utf-8"), "new skill\n")
        self.assertEqual((self.dest / "sub" / "note.txt").read_text(encoding="utf-8"), "nested\n")
        self.assertTrue((self.dest / MARKER).is_file())
        self.assertEqual(self.backups(), [])

    def test_unmanaged_destination_is_backed_up(self):
        self.dest.mkdir()
        (self.dest / "mine.txt").write_text("user data\n", encoding="utf-8")
        result = run_install_into(self.src, self.dest)
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = self.backups()
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "mine.txt").read_text(encoding="utf-8"), "user data\n")
        self.assertFalse((backups[0] / MARKER).exists())
        self.assertTrue((self.dest / MARKER).is_file())
        self.assertFalse((self.dest / "mine.txt").exists())
        self.assertEqual((self.dest / "SKILL.md").read_text(encoding="utf-8"), "new skill\n")

    def test_managed_destination_is_replaced_without_backup(self):
        self.dest.mkdir()
        (self.dest / MARKER).touch()
        (self.dest / "stale.txt").write_text("old\n", encoding="utf-8")
        (self.dest / "SKILL.md").write_text("old skill\n", encoding="utf-8")
        result = run_install_into(self.src, self.dest)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.dest / "stale.txt").exists())
        self.assertEqual((self.dest / "SKILL.md").read_text(encoding="utf-8"), "new skill\n")
        self.assertTrue((self.dest / MARKER).is_file())
        self.assertEqual(self.backups(), [])

    def test_same_directory_keeps_source(self):
        result = run_install_into(self.src, self.src)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.src / "SKILL.md").read_text(encoding="utf-8"), "new skill\n")
        self.assertEqual((self.src / "sub" / "note.txt").read_text(encoding="utf-8"), "nested\n")
        self.assertTrue((self.src / MARKER).is_file())

    def test_missing_source_fails(self):
        result = run_install_into(self.root / "absent", self.dest)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing source directory", result.stderr)
        self.assertFalse(self.dest.exists())


if __name__ == "__main__":
    unittest.main()
