from typing import List, Union, Dict, Sequence, TypeVar, Type
from ByteCode import load_interpreter, update_interpreter
from Tools import util


class BlockExtension:
    def __init__(self, name: str, path: str, abs_path: bool, working_dir: str, file_extension: str = "",
                 access_to_interpreter: bool = False, sub_thread: bool = True):
        self.name = name
        self.path = path
        self.abs_path = abs_path
        self.working_dir = working_dir
        self.file_extension = file_extension
        self.access_to_interpreter = access_to_interpreter
        self.sub_thread = sub_thread

        self.failed_to_load = False
        self.code = ""
        self.load_code()

    def load_code(self):
        try:
            with open(
                    f"{util.lang_get_path(self.path, self.abs_path, self.working_dir)}.{self.file_extension}") as file:
                self.code = file.read()
        except FileNotFoundError:
            self.failed_to_load = True


_T = TypeVar("_T", bound=type)


class ArgValue:
    def __init__(self, real_type: Union[Type[_T], type], real_value: Union[_T, object]):
        assert isinstance(real_value, real_type)
        self.real_type = real_type
        self.real_value = real_value

    def get(self):
        return self.real_value


class StringValue(ArgValue):
    def __init__(self, real_value: str):
        super().__init__(str, real_value)


class NumberValue(ArgValue):
    def __init__(self, real_value: Union[int, float]):
        super().__init__(float, float(real_value))


class BlockValue(ArgValue):
    def __init__(self, real_value: "Block", expected_value: _T):
        super().__init__(Block, real_value)
        self.expected_value = expected_value


class BlockArg:
    def __init__(self, arg_value: ArgValue):
        self.arg_value = arg_value

    def get_val(self):
        return self.arg_value.get()


class BlockArgs:
    def __init__(self, args: Sequence[BlockArg]):
        self.args = args

    def __getitem__(self, index: Union[int, slice]):
        return self.args[index]

    get = __getitem__


class BlockInfo:
    def __init__(self, name: str, byte_code: List[int],
                 constants: List[Union[str, int, bool, List[str, int, bool, List[...], Dict[str, ...]], Dict[
                     str, Union[str, int, bool, List[...], Dict[str, ...]]]]],
                 extensions: List[BlockExtension]):
        self.name = name
        self.byte_code = byte_code
        self.constants = constants
        self.extensions = extensions


class Block:
    def __init__(self, info: BlockInfo, args: BlockArgs):
        self.info = info
        self.args = args
        self.interpreter = load_interpreter(self.info)
        update_interpreter(self.interpreter, self.args)

