from collectors.collector import Collector


class HashCollector(Collector):
    def __init__(self, path=None, data=None, autoload: bool = False):
        collector_data = data if data is not None else {}
        super().__init__(path, collector_data, autoload)

    def __iter__(self):
        return self

    def __next__(self):
        if self._counter < self.count:
            self._counter += 1
            return next(self._collector)
        else:
            raise StopIteration

    def append(self, key=None, data=None, error=None):
        super().append(key, data, error)
        if key in self._collector.keys():
            self._collector[self._current_key] = (self._current_data, self._current_errors)
        else:
            self._collector.setdefault(key, [self._current_data, self._current_errors])

    def remove(self, key):
        if key in self._collector.keys():
            del self._collector[key]

    def get_keys(self):
        if self._collector is not None:
            return list(self._collector.keys())

    def get_error_count(self, key):
        return len(self._collector.get(key)[1])

    def get_data(self, key):
        data = self._collector.get(key)
        return data

    def get_status(self, key) -> bool:
        error_len = self.get_error_count(key)
        if error_len == 0:
            return True
        return False

    def get_errors(self, key) -> []:
        values = self._collector.get(key)
        if values is None:
            return []
        errors = values[1]
        return errors

    def select_by_status(self, status: bool) -> {}:
        result = {k: v for k, v in self._collector.items() if self.get_status(k) is status}
        return result

    @property
    def data(self) -> []:
        result = []
        for k, v in self._collector.items():
            result.append((k, v[0]))
        return result

    @property
    def keys(self):
        return self.get_keys()
