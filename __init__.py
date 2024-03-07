from .node import *

NODE_CLASS_MAPPINGS = {
    "Loop": Loop,
    "LoopStart": LoopStart,
    "LoopEnd": LoopEnd
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoopEnd": "LoopEnd",
    "LoopStart": "LoopStart",
    "LoopEnd": "LoopEnd"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
