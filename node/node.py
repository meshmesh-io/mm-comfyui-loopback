import torch

class Loop:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}

    RETURN_TYPES = ("LOOP",)
    FUNCTION = "run"
    CATEGORY = "loopback"

    def run(self):
        return (self,)

class LoopStart:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"first_loop": s.RETURN_TYPES, "loop": ("LOOP",)}}

    RETURN_TYPES = ()
    FUNCTION = "run"
    CATEGORY = "loopback"

    def run(self, first_loop, loop):
        if hasattr(loop, 'next'):
            return (loop.next,)
        return (first_loop,)

    @classmethod
    def IS_CHANGED(s, first_loop, loop):
        if hasattr(loop, 'next'):
            return id(loop.next)
        return float("NaN")

class LoopEnd:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "send_to_next_loop": s.LOOP_TYPE, "loop": ("LOOP",) }}

    RETURN_TYPES = ()
    LOOP_TYPE = ()
    FUNCTION = "run"
    CATEGORY = "loopback"
    OUTPUT_NODE = True

    def run(self, send_to_next_loop, loop):
        loop.next = send_to_next_loop
        return ()


class LoopStart_SEGIMAGE:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"loop": ("LOOP",), "image": ("IMAGE",)}}

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "loopback"

    idx = 0
    images_list = None
    def run(self, loop, image):
        if self.images_list is None:
            self.images_list = [image[i] for i in range(image.size(0))]
        if hasattr(loop, 'next'):
            self.idx += 1
            print("LoopStart_SEGIMAGE first run", self.idx)
            loop.next = self.images_list[self.idx]
            return (loop.next,)
        print("LoopStart_SEGIMAGE first run", self.idx)
        return (self.images_list[self.idx],)

    @classmethod
    def IS_CHANGED(s,loop):
        print("LoopStart_SEGIMAGE IS_CHANGED")
        print("loop", loop)
        if hasattr(loop, 'next') and hasattr(loop, 'trigger') and loop.trigger == True:
            loop.trigger = False
            return id(loop.next)
        return float("NaN")

class LoopEnd_SEGIMAGE:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "send_to_next_loop": ("IMAGE",), "loop": ("LOOP",) }, "optional": {"image": ("IMAGE",)}}

    RETURN_TYPES = ()
    LOOP_TYPE = ()
    FUNCTION = "run"
    CATEGORY = "loopback"
    OUTPUT_NODE = True

    def run(self, send_to_next_loop, loop, image):
        print("LoopEnd_SEGIMAGE run")
       
        if image is not None:
            loop.next = send_to_next_loop
            loop.trigger = True
            image = None
            return ()


NODE_CLASS_MAPPINGS = {
    "Loop": Loop,
    "LoopStart": LoopStart,
    "LoopEnd": LoopEnd,
    "LoopStart_SEGIMAGE": LoopStart_SEGIMAGE,
    "LoopEnd_SEGIMAGE": LoopEnd_SEGIMAGE
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "LoopEnd": "LoopEnd",
    "LoopStart": "LoopStart",
    "LoopEnd": "LoopEnd",
    "LoopStart_SEGIMAGE": "LoopStart_SEGIMAGE",
    "LoopEnd_SEGIMAGE": "LoopEnd_SEGIMAGE"
}

def addLoopType(t):
    NODE_CLASS_MAPPINGS["LoopStart_" + t] = type("LoopStart_" + t, (LoopStart, ), { "RETURN_TYPES": (t,) })
    NODE_CLASS_MAPPINGS["LoopEnd_" + t] = type("LoopEnd_" + t, (LoopEnd, ), { "LOOP_TYPE": (t,) })
    NODE_DISPLAY_NAME_MAPPINGS["LoopStart_" + t] = ["LoopStart_" + t]
    NODE_DISPLAY_NAME_MAPPINGS["LoopEnd_" + t] = ["LoopEnd_" + t]


#SEGS

# ComfyUI types
#addLoopType("IMAGE")
addLoopType("CONDITIONING")
addLoopType("LATENT")
addLoopType("MASK")
addLoopType("MODEL")

#addLoopType("SEGS")

# These don't work for some reason :/
# addLoopType("FLOAT")
addLoopType("NUMBER")
addLoopType("STR")

# Derfuu nodes use these types
addLoopType("FlOAT")
addLoopType("INTEGER")
addLoopType("TUPLE")

# WAS nodes use these types
addLoopType("ASCII")
addLoopType("STRING")

# Feel free to add more loopback node types here
