from abc import ABC, abstractmethod
import logging
import json
import os
import pickle
from datetime import datetime


logging.basicConfig()
logger = logging.getLogger()


class Collector(ABC):
    def __init__(self, path=None):
        self._path = path
        self._is_path_valid = True if os.path.exists(path) else False
        self._is_data_loaded = False
        self._success_append = 0
        self._error_append = 0

        self._counter = 0

        self._meta = {}
    # def to_stack(self, status: bool, data, key=None, error=None):
    #     k = key if key is not None else uuid.uuid4().hex
    #     self.__stack.append((status, data, error, k))

    # def to_problem(self, problem, source=None):
    #     self.__problem_stack.append((source, problem))

    @abstractmethod
    def save_as_binary(self):
        logger.debug("Saving to binary file" + self._path)
        pass
        #
        # pickle.dump(self._internal_collector, open(self._path, 'wb'))

    @abstractmethod
    def save_as_json(self):
        pass

    @abstractmethod
    def load_from_binary(self):
        logger.debug("Loaded data from binary file " + self._path)
        if os.path.exists(self._path):
            return pickle.load(open(self._path, 'rb'))
        logger.warning("File {} doesn't exist".format(self._path))

    @abstractmethod
    def load_from_json(self, hook=None):
        if self._is_path_valid:
            logger.debug("Loaded data from json file " + self._path)
            try:
                with open(self._path, 'rt') as handle:
                    data = json.load(handle, object_hook=hook)
            except json.JSONDecodeError:
                logger.warning("Error loading data from file " + self._path)
                return None
            else:
                return data
        return None
    # def select_from_stack(self, key=None, state: bool = True, errors: bool = False) -> []:
    #     if key is None:
    #         if errors:
    #             result = [i for i in self.__stack if i[0] == state and len(i(2)) > 0]
    #         else:
    #             result = [i for i in self.__stack if i[0] == state and len(i(2)) == 0]
    #     else:
    #         if errors:
    #             result = [i for i in self.__stack if i[4] == key and i[0] == state and len(i(2)) > 0]
    #         else:
    #             result = [i for i in self.__stack if i[4] == key and i[0] == state and len(i(2)) == 0]
    #     return result

    @abstractmethod
    def append(self, data):
        pass

    @abstractmethod
    def remove(self, bs_id):
        pass

    @abstractmethod
    def get_error_count(self, id):
        pass

    @abstractmethod
    def get_errors(self, id):
        pass

    @abstractmethod
    def get_data(self, key):
        pass

    @property
    @abstractmethod
    def data(self) -> []:
        pass

    @property
    @abstractmethod
    def keys(self) -> []:
        pass

    @property
    def success_append(self):
        return self._success_append

    @property
    def error_append(self):
        return self._error_append

    @property
    def total_append(self):
        return self._success_append + self._error_append

    @property
    @abstractmethod
    def count(self):
        pass
