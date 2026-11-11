"""Behavior checks for the protocol and shared state without opening sockets."""

import unittest

from scene import Scene


class SceneRulesTests(unittest.TestCase):
    def test_valid_absolute_position_updates_one_shared_revision(self):
        scene = Scene()
        for revision, x in enumerate((0, 100, 40), start=1):
            result = scene.apply({"id": f"a-{revision}", "action": "set_x", "x": x})
            self.assertEqual(result, {"type": "ack", "id": f"a-{revision}", "revision": revision})
            self.assertEqual(scene.snapshot(), {"type": "state", "x": x, "revision": revision})

    def test_invalid_messages_never_mutate_shared_state(self):
        scene = Scene()
        valid = {"id": "a-1", "action": "set_x", "x": 30}
        for invalid in (None, [], {}, {**valid, "x": True}, {**valid, "x": 100.5},
                        {**valid, "x": -1}, {**valid, "x": 101}, {**valid, "x": "30"},
                        {**valid, "id": ""}, {**valid, "id": 4}, {**valid, "id": "a" * 49},
                        {**valid, "action": "jump"}, {**valid, "extra": 1}):
            with self.subTest(invalid=invalid):
                before = scene.snapshot()
                with self.assertRaises(ValueError):
                    scene.apply(invalid)
                self.assertEqual(scene.snapshot(), before)

    def test_repeating_position_has_same_position_but_is_still_another_command(self):
        scene = Scene()
        action = {"id": "same-id", "action": "set_x", "x": 20}
        scene.apply(action)
        scene.apply(action)
        self.assertEqual(scene.snapshot()["x"], 20)
        self.assertEqual(scene.snapshot()["revision"], 2)

    def test_restarting_scene_resets_ram_and_snapshot_is_a_copy(self):
        scene = Scene()
        snapshot = scene.snapshot()
        snapshot["x"] = 0
        self.assertEqual(scene.snapshot()["x"], 50)
        scene.apply({"id": "once", "action": "set_x", "x": 20})
        self.assertEqual(Scene().snapshot(), {"type": "state", "x": 50, "revision": 0})


if __name__ == "__main__":
    unittest.main()
