from typing import Sequence, Optional, Dict, Callable, Tuple, List, Set, Union, Type
from threading import Thread
from Tools import BiDirectionalList


class ByteCodeInterpreter:
    settings: ByteCodeSettings
    external_handlers: ByteCodeExternalHandlers
    code: List[int]
    current_pos: int
    current_command: int
    current_command_args: Sequence[int]
    memory: ByteCodeMemory
    exception: Optional[ByteCodeException]
    catchable: bool
    bytecode_command_class: Type[ByteCodeCommand]

    def __init__(self, settings: "ByteCodeSettings", external_handlers: "ByteCodeExternalHandlers",
                 code: Union[bytes, List[int]]):
        ...

    @property
    def command(self) -> ByteCodeCommandRunner: ...

    def run(self): ...

    def get_fail(self, cause: Tuple[str, Sequence[int], Optional["ByteCodeException"]]) -> "ByteCodeException": ...

    def _fail(self, cause: Tuple[str, Sequence[int], Optional["ByteCodeException"]]): ...

    def _reset_command_info(self): ...

    def fail(self, desc: str): ...

    def exec_current_command(self): ...


class ByteCodeSettings:
    interpreter: ByteCodeInterpreter

    def __init__(self, interpreter: ByteCodeInterpreter = None): ...


class ByteCodeException:
    command: int
    arguments: Sequence[int]
    position: int
    cause: str
    sub_exception: Optional["ByteCodeException"]

    def __init__(self, command: int, arguments: Sequence[int], position: int, cause: str,
                 sub_exception: Optional["ByteCodeException"] = None): ...

    def text(self) -> str: ...


class ByteCodeCommandRunner:
    interpreter: ByteCodeInterpreter
    command: int

    def __init__(self, interpreter: ByteCodeInterpreter, command: int): ...

    def run(self, args: Sequence[int]): ...


class ByteCodeCommand:
    commands: Dict[int, "ByteCodeCommand"]
    code: int
    args_len: int
    action: "ByteCodeCommandAction"
    interpreter: ByteCodeInterpreter

    def __init__(self, code: int, args_len: int, action: "ByteCodeCommandAction", interpreter: ByteCodeInterpreter):
        ...

    def __new__(cls, *args, **kwargs) -> "ByteCodeCommand": ...

    def run(self, args: Sequence[int]): ...


class ByteCodeCommandAction:
    action: Callable[[Callable[[str], ...], Sequence[int]], Optional[str]]
    command: Optional[ByteCodeCommand]
    args_size: int

    def __init__(self, action: Callable[[Callable[[str], ...], Sequence[int]], Optional[str]],
                 command: Optional[ByteCodeCommand] = None): ...

    def run(self, fail: Callable[[str], ...], args: Sequence[int]): ...


class ByteCodeMemory:
    interpreter: ByteCodeInterpreter
    consts_stack: BiDirectionalList[ Union[str, int, bool, List[str, int, bool, List[...], Dict[str, ...]],
                                           Dict[str, Union[str, int, bool, List[...], Dict[str, ...]]]]]
    operating_on: BiDirectionalList
    variables: Dict[str, int]
    memory: Dict[int, ByteCodeObject]

    def __init__(self, interpreter: ByteCodeInterpreter): ...

    def load_constants(self, constants: Sequence[Union[str, int, float, bool, list, None]]): ...

    def get_object_from_memory(self, ref: int) -> ByteCodeObject: ...


class ByteCodeObject:
    memory: ByteCodeMemory
    obj_class: int
    values: Dict[str, int]

    def __init__(self, memory: ByteCodeMemory, obj_class: int, values: Dict[str, int]): ...


class ByteCodeObjectClass(ByteCodeObject):
    inst_magic: Dict[str, int]

    def __init__(self, memory: ByteCodeMemory, obj_class: int, values: Dict[str, int], inst_magic: Dict[str, int]): ...


class ByteCodeExternalHandlers:
    interpreter: ByteCodeInterpreter
    handlers: Set["ExternalHandler"]

    def __init__(self, interpreter: ByteCodeInterpreter = None): ...

    def add(self, exec_code: str, access_to_interpreter: bool = False, sub_thread: bool = True): ...

    def run_handlers(self): ...


class ExternalHandler:
    interpreter: ByteCodeInterpreter
    exec_code: str
    access_to_interpreter: bool
    sub_thread: bool
    api: ExternalHandlerApi
    handler_locals: Dict[str, ExternalHandlerApi]

    def __init__(self, interpreter: ByteCodeInterpreter, exec_code: str, access_to_interpreter: bool = False,
                 sub_thread: bool = True): ...

    def handler_exec(self): ...

    def run(self): ...

    def add_task(self, task: Sequence[int]): ...


class ExternalHandlerApi:
    interpreter: Optional[ByteCodeInterpreter]
    tasks: List[Sequence[int]]

    def __init__(self, interpreter: Optional[ByteCodeInterpreter] = None): ...

    def get_task(self) -> Union[Sequence[int], bool]: ...

    def add_task(self, info: Sequence[int]): ...

    def pop_task(self) -> Sequence[int]: ...
