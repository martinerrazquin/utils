class defaultdict_key(dict):
    """Good ol' defaultdict from collections library but the default
    factory method receives the key value as an argument."""

    def __init__(self, default_factory_with_key):
        super(defaultdict_key, self).__init__()
        self.factory = default_factory_with_key

    def __missing__(self, key):
        self[key] = self.factory(key)
        return self[key]
