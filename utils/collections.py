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
    are not exactly the expected ones. Regardless of this value, all the required keys are 
    always expected.
    """
    def __init__(self, keys: Iterable[Hashable]|None =None, raise_mismatch: bool = True):
        self.raise_mismatch = raise_mismatch
        if keys is not None:
            self.keys = set(keys)
            self.d = {k: [] for k in self.keys}
        else:
            self.keys = None
            self.d = None

    def append(self, item: dict[Hashable, Any]):
        received_keys = set(item.keys())
        if self.keys == None:
            self.keys = received_keys
            self.d = {k:[v] for k,v in item.items()}
            return
        if received_keys != self.keys and self.raise_mismatch:
            raise KeyError(f"Expected keys {self.keys}, got {received_keys}")
        if received_keys < self.keys:
            raise KeyError(f"Missing keys {self.keys - received_keys}")
        for k in self.keys:
            self.d[k].append(item[k])

    def export(self):
        return self.d
            


