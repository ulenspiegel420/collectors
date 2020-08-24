import json
from datetime import datetime


def load_json_file(path):
    try:
        with open(path, 'rt') as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return


class Problem(Exception):
    def __init__(self, src, msg, level='ERROR', date=None, state='new'):
        self.__source = src
        self.__msg = msg
        self.__date = datetime.utcnow() if date is None else datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        self.__is_sent = True if state == 'sent' else False
        self.__state = state
        self.__level = level

    def __eq__(self, other):
        if isinstance(other, Problem):
            return self.__source == other.__source and self.__msg == other.__msg
        return False

    def __repr__(self):
        return 'Source: {}, Problem: {}'.format(self.__source, self.__msg)

    @property
    def source(self) -> str:
        return self.__source

    @property
    def msg(self) -> str:
        return self.__msg

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def is_sent(self) -> bool:
        return self.__is_sent

    @is_sent.setter
    def is_sent(self, value):
        if not isinstance(value, bool):
            raise TypeError
        self.__is_sent = value

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str):
        self.__state = value

    @property
    def level(self) -> str:
        return self.__level


def as_problem(dct):
    if '__problem__' in dct:
        return Problem(dct['source'], dct['msg'], dct['level'], dct['date'], dct['state'])
    return dct


class ProblemEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Problem):
            return {'__problem__': True, 'source': o.source, 'level': o.level, 'msg': o.msg, 'state': o.state,
                    'date': o.date.strftime('%d.%m.%Y %H:%M:%S')}
        return json.JSONEncoder.default(self, o)