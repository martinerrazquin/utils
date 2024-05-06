from typing import Any, Hashable, Iterable


class defaultdict_key(dict):
    """Good ol' defaultdict from collections library but the default
    factory method receives the key value as an argument."""

    def __init__(self, default_factory_with_key):
        super(defaultdict_key, self).__init__()
        self.factory = default_factory_with_key

    def __missing__(self, key):
        self[key] = self.factory(key)
        return self[key]


class ListDictBuilder:
    """
    Somewhat like a Pandas DataFrame but you build it by iteratively
    appending rows, which is not how you want to build a pandas df.

    keys (optional): list-like of keys. If None, will be inferred from first item appended.
    raise_mismatch: whether to raise a KeyError when appending an item whose keys
    are not *exactly* the expected ones. If False, missing keys will be completed based
    on the fill_values parameter, but exceding keys will nonetheless raise
    fill_values: value with which to fill missing expected keys.  If it's a value, all missing
    keys will be filled with said value. If it's a dict, the fill value will be looked up by key.
    If a key is missing in both the fill_values dict and the item to be appended, will
    raise KeyError. Non-None values *require* the keys parameter to be passed.
    """

    def __init__(
        self,
        keys: Iterable[Hashable] | None = None,
        raise_mismatch: bool = True,
        fill_value: dict[Hashable | Any] | Any | None = None,
    ):
        if keys is not None:
            self.keys = set(keys)
            self.d = {k: [] for k in self.keys}
        else:
            if fill_value is not None:
                raise ValueError(
                    "fill_value is not None but keys were not explicitly declared"
                )
            self.keys = None
            self.d = None
        self.raise_mismatch = raise_mismatch
        match fill_value:
            case None:
                self.fill_value = {}
            case dict():
                self.fill_value = fill_value.copy()
            case _:
                self.fill_value = {k: fill_value for k in self.keys}

    def append(self, item: dict[Hashable, Any]):
        received_keys = set(item.keys())
        if self.keys == None:
            self.keys = received_keys
            self.d = {k: [v] for k, v in item.items()}
            return
        if received_keys != self.keys and self.raise_mismatch:
            raise KeyError(f"Expected keys {self.keys}, got {received_keys}")
        for k in self.keys:
            if k not in item and k not in self.fill_value:
                raise KeyError(f"Key {k} missing in item without a supplied fill value")
            self.d[k].append(item.get(k, self.fill_value.get(k)))

    def export(self):
        return self.d
