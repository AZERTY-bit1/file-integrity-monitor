import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fim import scan, compare  # noqa: E402


class TestFIM(unittest.TestCase):
    def test_detects_changes(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ("a.txt", "b.txt"):
                with open(os.path.join(d, n), "w") as f:
                    f.write(n)
            base = scan(d)
            with open(os.path.join(d, "a.txt"), "w") as f:
                f.write("changed")
            os.remove(os.path.join(d, "b.txt"))
            with open(os.path.join(d, "c.txt"), "w") as f:
                f.write("new")
            diff = compare(base, scan(d))
            self.assertEqual(diff, {"added": ["c.txt"], "deleted": ["b.txt"], "modified": ["a.txt"]})


if __name__ == "__main__":
    unittest.main()
