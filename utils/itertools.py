from functools import wraps


# credits to https://stackoverflow.com/a/62692540
class RepeatableGenerator:
    def __init__(self, gen, *args, **kwargs):
        self.gen = gen
        self.args = args
        self.kwargs = kwargs
        self.it = None

    def __iter__(self):
        self.it = self.gen(*self.args, **self.kwargs)
        return self

    def __next__(self):
        return next(self.it)


def repeatable(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return RepeatableGenerator(fn, *args, **kwargs)

    return wrapper


@repeatable
def pairs(iterable):
    return iter(zip(iterable[:-1], iterable[1:]))
