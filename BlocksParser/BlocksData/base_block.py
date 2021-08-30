from typing import List, Union, Dict
from ByteCode import load_interpreter


class BlockInfo:
    def __init__(self, name: str, byte_code: List[int],
                 constants: List[Union[str, int, bool, List[str, int, bool, List[...], Dict[str, ...]], Dict[
                     str, Union[str, int, bool, List[...], Dict[str, ...]]]]],
                 extensions: List[...]):
        self.name = name
        self.byte_code = byte_code
        self.constants = constants
        self.extensions = extensions


class BaseBlock:
    def __init__(self, info: BlockInfo):
        self.info = info
        self.interpreter = load_interpreter(self.info)
