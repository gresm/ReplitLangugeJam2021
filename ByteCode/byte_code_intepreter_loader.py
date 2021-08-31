from . import byte_code as bc
from BlocksParser import BlockInfo


def load_settings(block_settings: BlockInfo) -> bc.ByteCodeSettings:
    return bc.ByteCodeSettings()


def load_external_handlers(block_settings: BlockInfo) -> bc.ByteCodeExternalHandlers:
    bc_ext = bc.ByteCodeExternalHandlers()
    for extension in block_settings.extensions:
        if not extension.failed_to_load:
            bc_ext.add(extension.code, extension.access_to_interpreter, extension.sub_thread)
    return bc_ext


def load_interpreter(block_settings: BlockInfo) -> bc.ByteCodeInterpreter:
    return bc.ByteCodeInterpreter(bc.ByteCodeSettings(), load_external_handlers(block_settings),
                                  block_settings.byte_code)
