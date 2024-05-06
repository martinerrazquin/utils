import unittest
from utils.collections import ListDictBuilder


class TestListDictBuilder(unittest.TestCase):
    def test_build_complete_keys_passed(self):
        c1 = [1, 2, 3, 4]
        c2 = ["a", "b", "c", "d"]
        c3 = [True, False, True, False]
        keys = ["X", 5, ("a", "b")]

        expected = {k: c for k, c in zip(keys, (c1, c2, c3))}

        x = ListDictBuilder(keys)
        for x1, x2, x3 in zip(c1, c2, c3):
            item = {k: x for k, x in zip(keys, (x1, x2, x3))}
            x.append(item)
        result = x.export()
        self.assertDictEqual(expected, result)

    def test_build_complete_keys_inferred(self):
        c1 = [1, 2, 3, 4]
        c2 = ["a", "b", "c", "d"]
        c3 = [True, False, True, False]
        keys = ["X", 5, ("a", "b")]

        expected = {k: c for k, c in zip(keys, (c1, c2, c3))}

        x = ListDictBuilder()
        for x1, x2, x3 in zip(c1, c2, c3):
            item = {k: x for k, x in zip(keys, (x1, x2, x3))}
            x.append(item)
        result = x.export()
        self.assertDictEqual(expected, result)

    def test_mismatch_raises_when_enabled_extra(self):
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=True)
        with self.assertRaises(KeyError) as s:
            x.append({"X": 1, "Y": 2, "Z": 4})

    def test_mismatch_raises_when_enabled_missing(self):
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=True)
        with self.assertRaises(KeyError) as s:
            x.append({"X": 1})

    def test_mismatch_raises_when_disabled_missing_and_no_fill(self):
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=False)
        with self.assertRaises(KeyError) as s:
            x.append({"X": 1})

    def test_mismatch_no_raise_when_disabled_extra(self):
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=False)
        try:
            x.append({"X": 1, "Y": 2, "Z": 4})
        except KeyError:
            self.fail("KeyError was wrongfully raised.")

    def test_mismatch_no_raise_when_disabled_missing_with_fill(self):
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=False, fill_value=3)
        try:
            x.append({"X": 1})
        except KeyError:
            self.fail("KeyError was wrongfully raised.")

    def test_raises_when_no_keys_but_fill_passed(self):
        with self.assertRaises(ValueError) as s:
            x = ListDictBuilder(raise_mismatch=False, fill_value=5)

    def test_no_raise_when_keys_and_fill_passed(self):
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=False, fill_value=5)
        try:
            x.append({"X": 1})
        except KeyError:
            self.fail("KeyError was wrongfully raised.")

    def test_build_complete_fill_value_scalar(self):
        fill_v = 5
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=False, fill_value=fill_v)
        x.append({})

        expected = {"X": [fill_v], "Y": [fill_v]}

        result = x.export()
        self.assertDictEqual(expected, result)

    def test_build_complete_fill_value_dict(self):
        fill_v_x = 1
        fill_v_y = 2
        fill_dict = {"X": fill_v_x, "Y": fill_v_y}
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=False, fill_value=fill_dict)

        x.append({"X": 5})
        x.append({"Y": 6})

        expected = {"X": [5, fill_v_x], "Y": [fill_v_y, 6]}

        result = x.export()
        self.assertDictEqual(expected, result)

    def test_build_raises_fill_value_dict_missing_one_key(self):
        fill_dict = {"X": 3}
        x = ListDictBuilder({"X", "Y"}, raise_mismatch=False, fill_value=fill_dict)

        x.append({"Y": 3})

        with self.assertRaises(KeyError):
            x.append({"X": 3})
