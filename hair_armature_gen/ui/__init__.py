import bpy
from .panel import HAIR_RIG_PT_main

_classes = (HAIR_RIG_PT_main,)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
