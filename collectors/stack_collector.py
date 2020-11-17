from abc import ABC

from collectors.collector import Collector


class StackCollector(Collector, ABC):
    def __init__(self, path: str, data=None, autoload: bool = False):
        super().__init__(path, data, autoload)
        if self._collector is None: self._collector = []

    def __iter__(self):
        return self

    def __next__(self):
        if self._counter < self.count:
            self._counter += 1
            return self._collector[self._counter - 1]
        else:
            raise StopIteration

    def __add__(self, other):
        self._collector.extend(other._collector)
        self._success_append += other._success_append
        self._error_append += other._error_append
        return self

    def append(self, id=None, data=None, error=None):
        super().append(id, data, error)
        self._collector.append((self._current_key, self._current_data, self._current_errors))

    def get_error_count(self, id) -> int or None:
        item = [i for i in self._collector if i[0] == id]
        if len(item) != 1:
            return None
        return len(item[2])

    def get_errors(self, id):
        pass

    def get_data(self, key):
        result = []
        for i in self._collector:
            if i[0] == key:
                result.append(i[1])
        return result

    @property
    def data(self):
        return self._collector

    @property
    def keys(self):
        result = [i[0] for i in self._collector]
        return result