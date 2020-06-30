from collectors.collector import Collector
from collectors import core


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

    # def load(self) -> {} or None:
    #     super().load()
    #     data = core.load_json_file(self._path)
    #     self._collector = data if data is not None and isinstance(data, dict) else {}

    def append(self, key=None, data=None, error=None):
        super().append(key, data, error)
        if key in self._collector.keys():
            self._collector[self._current_key] = (self._current_data, self._current_errors)
        else:
            self._collector.setdefault(key, (self._current_data, self._current_errors))

    def remove(self, bs_id):
        del self._collector[bs_id]

    def get_keys(self):
        if self._collector is not None:
            return list(self._collector.keys())

    def get_error_count(self, id):
        return len(self._collector.get(id)[1])

    def get_data(self, bs_id):
        data = self._collector.get(bs_id)
        return data

    def get_status(self, id) -> bool:
        error_len: int = self.get_error_count(id)
        if error_len == 0:
            return True
        return False

    def get_errors(self, id) -> []:
        result = [v[1] for k, v in self._collector.items() if k == id and len(v[1]) != 0]
        if len(result) == 0:
            return None
        return result

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
