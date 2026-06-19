import bpy
from .generate_rig import HAIR_RIG_OT_generate, HAIR_RIG_OT_clear

_classes = (
    HAIR_RIG_OT_generate,
    HAIR_RIG_OT_clear,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
