"""Standard-library tests for the pure function and the local host policy."""

import unittest

from trace import add, check_call, simulate


class TraceTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add(-2, 2), 0)

    def test_add_rejects_nonintegers(self):
        for a in (True, "3", 3.0, None):
            with self.subTest(a=a), self.assertRaises(TypeError):
                add(a, 4)

    def test_host_rejects_unknown_tool_before_dispatch(self):
        self.assertIn("blocked", check_call("overwrite", {"path": "work.txt"}))
        self.assertIn("nothing dispatched", simulate("overwrite", {"path": "work.txt"}))

    def test_host_rejects_missing_extra_and_wrong_types(self):
        for args in ({"a": 3}, {"a": 3, "b": 4, "path": "work.txt"},
                     {"a": "3", "b": 4}, {"a": True, "b": 4}, None):
            with self.subTest(args=args):
                self.assertIn("invalid input", check_call("add", args))

    def test_allowed_call(self):
        self.assertIsNone(check_call("add", {"a": 3, "b": 4}))
        self.assertEqual(simulate("add", {"a": 3, "b": 4}),
                         "local function result: 7")


if __name__ == "__main__":
    unittest.main()
