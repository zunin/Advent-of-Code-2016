from collections import namedtuple


class BaseInputParser:
    def __init__(self, file_name="input.txt"):
        self.file_name = file_name

    @property
    def lines(self):
        with open(self.file_name, "rt") as input_file:
            for line in input_file:
                yield line


class DataClass:
    _data = None

    def __init__(self, **kwargs):
        self.model = namedtuple(self.__class__.__name__+"Data", list(kwargs.keys()))
        self.data = self.model(**kwargs)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, cls: namedtuple):
        self._data = cls
        for name, value in cls._asdict().items():
            self.__setattr__(name, value)

    def __repr__(self):
        return self.data.__repr__().replace(
            self.model.__name__,
            self.__class__.__name__
        )

    def __eq__(self, other):
        return self.data.__eq__(other.data)

    def __lt__(self, other):
        return self.data.__lt__(other.data)

    def __hash__(self):
        return self.data.__hash__()