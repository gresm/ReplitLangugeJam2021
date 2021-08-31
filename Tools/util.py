from typing import List, Union, Dict, Tuple
from types import FunctionType
import os


word_chars = {chr(i) for i in range(65, 91)}.union(
    {chr(i) for i in range(97, 123)}.union({chr(i) for i in range(48, 58)}))

end_line: str = "\n"
sequence_char = "\""


def lang_split(txt: str) -> List[List[str]]:
    ret = []

    for line in txt.split(end_line):
        lno = []
        cur = ""
        seq = False
        for char in line:
            if char == sequence_char:
                seq = not seq
            elif seq:
                cur += char
                continue

            if char in word_chars:
                cur += char
            elif not char.isspace():
                if cur:
                    lno.append(cur)
                lno.append(char)
                cur = ""
            else:
                if cur:
                    lno.append(cur)
                cur = ""
        ret.append(lno)
    return ret


def lang_get_path(path: str, absolute: bool = False, working_dir: str = ""):
    if absolute:
        if working_dir:
            return os.path.join(working_dir, os.path.join(*path.split(".")))
        return os.path.abspath(os.path.join(*path.split(".")))
    else:
        return os.path.join(*path.split("."))


def _fix_args(args: tuple, kwargs: dict, arg_place: Union[str, int], val):
    if isinstance(arg_place, int):
        if arg_place == len(args):
            args = args + (val,)
        else:
            args = args
            args = tuple([args[v] if v != arg_place else val for v in range(len(args))])
    else:
        kwargs = kwargs.copy()
        kwargs[arg_place] = val
    return args, kwargs


def connect(arg_place: Union[int, str]):
    ret = _Connector(arg_place)
    return ret.grab_after


class _Connector:
    def __init__(self, arg_place: Union[str, int], func: FunctionType = None):
        self.func = func
        self.arg_place = arg_place
        self._cached: Dict[Tuple[object, type], _BoundConnector] = {}
        self.connected = False
        self.value = None
        self.owner = None

    def __get__(self, instance: object, owner: type):
        self.owner = owner
        if instance:
            if (instance, owner) in self._cached:
                return self._cached[instance, owner]
            self._cached[instance, owner] = _BoundConnector(self, instance, owner)
            return self._cached[instance, owner]
        else:
            return self

    def __call__(self, *args, **kwargs):
        args, kwargs = self._fixed_args(args, kwargs)
        return self.__base_call__(*args, **kwargs)

    def __base_call__(self, *args, **kwargs):
        if not self.func:
            raise ValueError("_Connector object not correctly initialized")
        return self.func(*args, **kwargs)

    def _fixed_args(self, args: tuple, kwargs: dict):
        args, kwargs = _fix_args(args, kwargs, 0, self.owner)
        return _fix_args(args, kwargs, 1, self.value)

    def grab_after(self, func: FunctionType):
        self.func = func
        return self

    def connect(self, val):
        self.value = val
        self.connected = True


class _BoundConnector:
    def __init__(self, connector: _Connector, instance: object, owner: type):
        self.connector = connector
        self.instance = instance
        self.owner = owner
        self.value = None

    def __call__(self, *args, **kwargs):
        args, kwargs = self._fixed_args(args, kwargs)
        return self.connector.__base_call__(*args, **kwargs)

    def _fixed_args(self, args: tuple, kwargs: dict):
        args, kwargs = _fix_args(args, kwargs, 0, self.instance)
        return _fix_args(args, kwargs, 1, self.value)

    def connect(self, val):
        self.value = val
