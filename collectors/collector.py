from abc import ABC, abstractmethod
import logging
import json
import os
import uuid
import pickle


logging.basicConfig()
logger = logging.getLogger(__name__)


class Collector:
    def __init__(self, path, data, autoload: bool = False):
        self._path: str = path
        self.__problem_stack = []
        self.__stack = []
        self._collector = data
        self._success_append = 0
        self._error_append = 0

        self._current_data = None
        self._current_errors = []
        self._current_key = None

        self._counter = 0
        self._loaded_data = None

        if autoload:
            if not os.path.exists(self._path):
                open(self._path, 'a').close()
            self.load()

    def to_stack(self, status: bool, data, key=None, error=None):
        k = key if key is not None else uuid.uuid4().hex
        self.__stack.append((status, data, error, k))

    def to_problem(self, problem, source=None):
        self.__problem_stack.append((source, problem))

    def save(self):
        logger.debug(f"Saving from the collector to {self._path}")
        pickle.dump(self._collector, open(self._path, 'wb'))

    def load(self):
        logger.debug(f"Loading to the collector from {self._path}")
        self._collector = pickle.load(open(self._path, 'rb'))

    def select_from_stack(self, key=None, state: bool = True, errors: bool = False) -> []:
        if key is None:
            if errors:
                result = [i for i in self.__stack if i[0] == state and len(i(2)) > 0]
            else:
                result = [i for i in self.__stack if i[0] == state and len(i(2)) == 0]
        else:
            if errors:
                result = [i for i in self.__stack if i[4] == key and i[0] == state and len(i(2)) > 0]
            else:
                result = [i for i in self.__stack if i[4] == key and i[0] == state and len(i(2)) == 0]
        return result

    @abstractmethod
    def append(self, id=None, data=None, error=None):
        self._current_key = None
        self._current_errors.clear()
        self._current_data = None

        if error is None:
            self._success_append += 1
        else:
            self._error_append += 1

        self._current_key = id if id is not None else uuid.uuid4().hex
        if error is not None:
            self._current_errors.append(error)
        self._current_data = data

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
    def count(self):
        return len(self._collector)