import uuid
import logging
import json
from collectors.collector import Collector


logging.basicConfig()
logger = logging.getLogger()


class HashCollector(Collector):
    def save_as_binary(self):
        pass

    def load_from_binary(self):
        pass

    @property
    def count(self):
        pass

    def __init__(self, data=None, path=None):
        super(HashCollector, self).__init__(path)
        self._internal_collector = {}
        if data is not None:
            if not isinstance(data, dict):
                raise ValueError("Data must be dict, but one have {} type".format(str(type(data))))
            for k, d in data.items():
                self.append(d, k)

    def __iter__(self):
        return self

    def __next__(self):
        if self._counter < self.count:
            self._counter += 1
            return next(self._internal_collector)
        else:
            raise StopIteration

    def append(self, data, key=None):
        super().append(data)
        if key in self._internal_collector.keys():
            if key is not None:
                current_key = key
                current_data = self.get_data(key)
            else:
                current_key = uuid.uuid4().hex
                current_data = []

            self._internal_collector[current_key] = [current_data + data, self._meta]
        else:
            self._internal_collector.setdefault(key, [data, self._meta])

    def remove(self, key):
        if key in self._internal_collector.keys():
            del self._internal_collector[key]

    def get_keys(self):
        if self._internal_collector is not None:
            return list(self._internal_collector.keys())

    def get_error_count(self, key):
        return len(self._internal_collector.get(key)[1])

    def get_data(self, key):
        if len(self._internal_collector) > 0:
            if key in self._internal_collector:
                data = self._internal_collector.get(key)[0]
                return data

    def get_status(self, key) -> bool:
        error_len = self.get_error_count(key)
        if error_len == 0:
            return True
        return False

    def get_errors(self, key) -> []:
        values = self._internal_collector.get(key)
        if values is None:
            return []
        errors = values[1]
        return errors

    def select_by_status(self, status: bool) -> {}:
        result = {k: v for k, v in self._internal_collector.items() if self.get_status(k) is status}
        return result

    def load_from_json(self, hook=None):
        data = super().load_from_json(hook)
        if data is not None:
            if not isinstance(data, dict):
                logger.warning('Bad content in json file')
            else:
                self._internal_collector = data
                self._is_data_loaded = True

    def save_as_json(self, encoder=None):
        with open(self._path, 'w') as handler:
            json.dump(self._internal_collector, handler, cls=encoder, sort_keys=True, indent=4)

    @property
    def data(self) -> []:
        result = []
        for k, v in self._internal_collector.items():
            result.append((k, v[0]))
        return result

    @property
    def keys(self):
        return self.get_keys()
