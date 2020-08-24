from collectors import HashCollector
from collectors.core import Problem, as_problem, ProblemEncoder
import json
import os


class ProblemCollector(HashCollector):
    def __init__(self, data_file, data=None, autoload=False):
        super(ProblemCollector, self).__init__(data_file, data)

        if autoload:
            if os.path.exists(data_file):
                with open(data_file, 'r') as handler:
                    data = json.load(handler, object_hook=as_problem)
                self._collector = data

    def append(self, key=None, data=None, error=None):
        problems = data if data is not None or isinstance(data, list) else []

        if key in self.keys:
            saved_problems = self.get_problems(key)
            for problem in problems:
                if problem not in saved_problems:
                    saved_problems.append(problem)
        else:
            super().append(key, problems, error)

    def get_problems(self, bs_id: str, src=None) -> []:
        data = self.get_data(bs_id)
        if data is None:
            return []
        if src is None:
            result = data[0]
        else:
            result = [i for i in data[0] if i.source == src]
        return result

    def exclude(self, bs_id, problems: []):
        if bs_id in self.keys:
            if len(problems) == 0:
                self.remove(bs_id)
            else:
                for problem in self.get_problems(bs_id):
                    if problem not in problems:
                        self._collector[bs_id].remove(problem)
                if self.get_data(bs_id) is None or len(self.get_data(bs_id)) == 0:
                    self.remove(bs_id)

    def exclude_by_source(self, bs_id, source):
        problems = self.get_problems(bs_id, source)
        for problem in problems:
            if problem.source == source:
                self._collector[bs_id][0].remove(problem)

    def has_problems(self, bs_id):
        if len(self.get_problems(bs_id)) == 0:
            return False
        return True

    def has_errors(self, bs_id) -> bool:
        if len(self.get_errors(bs_id)) == 0:
            return False
        return True

    def print(self, bs_id, state=None):
        data = self.get_problems(bs_id)
        problems = [i for i in data if state is not None and i.state == state] if state is not None else data
        if len(problems) == 0:
            print('\t\t', 'No problems.')
        counter = 1
        for p in problems:
            print('\t\t', str(counter)+')', 'source: ' + p.source + ', ', 'problem: ' + p.msg + ' , date:', p.date)
            counter += 1

    def print_all(self):
        print("Total problems: " + str(self.count) + "\n")
        counter = 1
        for bs_id in self.keys:
            print('\t #' + str(counter), bs_id)
            self.print(bs_id)
            counter += 1

    def get_unique_problems(self) -> []:
        result = []
        for values in list(self.problems.values()):
            for p in values:
                if p not in result:
                    result.append(p)
        return result

    def print_errors(self, bs_id: str):
        errors = self.get_errors(bs_id) if bs_id is not None else self.errors
        print("Errors:")
        for e in errors:
            print('\t', e)

    def save(self):
        with open(self._path, 'w') as handler:
            json.dump(self._collector, handler, cls=ProblemEncoder, sort_keys=True, indent=4)

    @property
    def errors(self) -> {}:
        result = {}
        for bs_id, data in self._collector.items():
            result[bs_id] = data[1]
        return result

    @property
    def problems(self):
        result = {}
        for k, v in self._collector.items():
            result[k] = v[0]
        return result