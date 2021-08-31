from typing import List, Union, Dict
from ByteCode import load_interpreter
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


class BlockArg:
    def __init__(self, block_type):
        self.block_type = block_type


class BlockArgs:
    def __init__(self, args):
        pass

        
    def get(self):
        args = []
        for block in self.args:
            args.append(block.get())
        return self.logic(args)




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
    def __init__(self, info: BlockInfo, args: List["BaseBlock"]):
        self.info = info
        self.interpreter = load_interpreter(self.info)
        self.args = BlockArgs(args)


