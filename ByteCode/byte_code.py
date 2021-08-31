from typing import Sequence, Optional, Dict, Callable, Tuple, List, Set, Union
from threading import Thread
from Tools import BiDirectionalList


class ByteCodeInterpreter:
    def __init__(self, settings: "ByteCodeSettings", external_handlers: "ByteCodeExternalHandlers",
                 code: Union[bytes, List[int]]):
        self.settings = settings
        self.settings.interpreter = self

        self.external_handlers = external_handlers
        self.external_handlers.interpreter = self

        self.code: List[int] = list(code)
        self.current_pos: int = 0
        self.current_command = -1
        self.current_command_args: Sequence[int] = ()
        self.memory = ByteCodeMemory(self)
        self.exception: Optional[ByteCodeException] = None
        self.catchable = True
        self.bytecode_command_class = ByteCodeCommand

    @property
    def command(self):
        return ByteCodeCommandRunner(self, self.current_command)

    def run(self):
        while self.current_pos < len(self.code):
            try:
                self.exec_current_command()
            except Exception as e:
                self.fail(f"While running command an exception occurred:"
                          f"{e.__class__} with description: {e.args}")

            try:
                self.external_handlers.run_handlers()
            except Exception as e:
                self.fail(f"While running external handlers, an exception occurred:\n"
                          f"{e.__class__} with description: {e.args}")

            if self.exception:
                break

            self._reset_command_info()

    def get_fail(self, cause: Tuple[str, Sequence[int], Optional["ByteCodeException"]]) -> "ByteCodeException":
        description = cause[0]
        args = cause[1]
        sub_exc = cause[2]
        return ByteCodeException(self.current_command, args, self.current_pos, description, sub_exc)

    def _fail(self, cause: Tuple[str, Sequence[int], Optional["ByteCodeException"]]):
        self.exception = self.get_fail(cause)

    def _reset_command_info(self):
        self.current_command_args = ()
        self.current_command = -1

    def fail(self, desc: str):
        self._fail((desc, self.current_command_args, self.exception))

    def exec_current_command(self):
        self.current_command = self.code[self.current_pos]

        if self.current_command not in ByteCodeCommand.commands:
            self.catchable = False
            self.fail("Unknown Command")
        else:
            command_obj = ByteCodeCommand.commands[self.current_command]

            current_pos = self.current_pos + 1
            cnt = 0
            lst_args: List[int] = []
            while current_pos < len(self.code) and cnt < command_obj.args_len:
                lst_args.append(self.code[current_pos])

                cnt += 1
                current_pos += 1

            self.current_pos = current_pos
            self.current_command_args = tuple(lst_args)


class ByteCodeSettings:
    def __init__(self, interpreter: ByteCodeInterpreter = None):
        self.interpreter = interpreter


class ByteCodeException:
    def __init__(self, command: int, arguments: Sequence[int], position: int, cause: str,
                 sub_exception: Optional["ByteCodeException"] = None):
        self.command = command
        self.arguments = arguments
        self.position = position
        self.cause = cause
        self.sub_exception = sub_exception

    def text(self) -> str:
        if self.sub_exception:
            return f"An Runtime Exception Occurred at: {self.position}, caused by: {self.command}\n" \
                   f"Description:\n{self.cause}\n" \
                   f"--------------------------\n" \
                   f"While Handling Above Exception, Other exception occurred:\n" \
                   f"{self.sub_exception.text()}"
        return f"An Runtime Exception Occurred at: {self.position}, caused by: {self.command}\n" \
               f"Description:\n{self.cause}"


class ByteCodeCommandRunner:
    def __init__(self, interpreter: ByteCodeInterpreter, command: int):
        self.interpreter = interpreter
        self.command = command

    def run(self, args: Sequence[int]):
        self.interpreter.bytecode_command_class.commands[self.command].run(args)


class ByteCodeCommand:
    commands: Dict[int, "ByteCodeCommand"] = {}

    def __init__(self, code: int, args_len: int, action: "ByteCodeCommandAction", interpreter: ByteCodeInterpreter):
        self.code = code
        self.args_len = args_len
        self.interpreter = interpreter
        self.action = action
        self.action.args_size = self.args_len
        self.action.command = self

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        cmd = kwargs["code"] if "code" in kwargs else args[0]
        cls.commands[cmd] = obj
        return obj

    def run(self, args: Sequence[int]):
        self.action.run(self.interpreter.fail, args)


class ByteCodeCommandAction:
    def __init__(self, action: Callable[[Callable[[str], ...], Sequence[int]], Optional[str]],
                 command: Optional[ByteCodeCommand] = None):
        self.action = action
        self.args_size: int = 0
        self.command: Optional[ByteCodeCommand] = command

    def run(self, fail: Callable[[str], ...], args: Sequence[int]):
        if len(args) == self.args_size:
            ret = self.action(fail, args)
            if ret:
                self.command.interpreter.fail(ret)
        else:
            self.command.interpreter.fail("Incorrect args size")


class ByteCodeMemory:
    def __init__(self, interpreter: ByteCodeInterpreter):
        self.interpreter = interpreter
        self.consts_stack: BiDirectionalList[
            Union[str, int, bool, List[str, int, bool, List[...], Dict[str, ...]], Dict[
                str, Union[str, int, bool, List[...], Dict[str, ...]]]]] = BiDirectionalList()
        self.operating_on: BiDirectionalList = BiDirectionalList()
        self.variables: Dict[str, int] = {}
        self.memory: Dict[int, ByteCodeObject] = {}

    def load_constants(self, constants: Sequence[Union[str, int, float, bool, list, None]]):
        self.consts_stack.push_all_from_first(constants)

    def get_object_from_memory(self, ref: int):
        if ref in self.memory:
            return self.memory[ref]


class ByteCodeObject:
    def __init__(self, memory: ByteCodeMemory, obj_class: int, values: Dict[str, int]):
        self.memory = memory
        self.obj_class = obj_class
        self.values = values


class ByteCodeObjectClass(ByteCodeObject):
    def __init__(self, memory: ByteCodeMemory, obj_class: int, values: Dict[str, int], inst_magic: Dict[str, int]):
        super().__init__(memory, obj_class, values)
        self.inst_magic = inst_magic


class ByteCodeExternalHandlers:
    def __init__(self, interpreter: ByteCodeInterpreter = None):
        self.handlers: Set["ExternalHandler"] = set()
        self.interpreter = interpreter

    def add(self, exec_code: str, access_to_interpreter: bool = False, sub_thread: bool = True):
        self.handlers.add(ExternalHandler(self.interpreter, exec_code, access_to_interpreter, sub_thread))

    def run_handlers(self):
        for handler in self.handlers:
            handler.run()


class ExternalHandler:
    def __init__(self, interpreter: ByteCodeInterpreter, exec_code: str, access_to_interpreter: bool = False,
                 sub_thread: bool = True):
        self.interpreter = interpreter
        self.exec_code = exec_code
        self.access_to_interpreter = access_to_interpreter
        self.sub_thread = sub_thread
        self.api = ExternalHandlerApi(self.interpreter if self.access_to_interpreter else None)
        self.handler_locals = {"api": self.api}

    def handler_exec(self):
        if len(self.api.tasks):
            exec(self.exec_code, None, self.handler_locals)

    def run(self):
        if self.sub_thread:
            thread = Thread(target=self.handler_exec)
            thread.start()
        else:
            self.handler_exec()

    def add_task(self, task: Sequence[int]):
        self.api.tasks.append(task)


class ExternalHandlerApi:
    def __init__(self, interpreter: Optional[ByteCodeInterpreter] = None):
        self.interpreter = interpreter
        self.tasks: List[Sequence[int]] = []

    def get_task(self) -> Union[Sequence[int], bool]:
        return self.tasks[0] if len(self.tasks) else False

    def add_task(self, info: Sequence[int]):
        self.tasks.append(info)

    def pop_task(self):
        return self.tasks.pop(0)
