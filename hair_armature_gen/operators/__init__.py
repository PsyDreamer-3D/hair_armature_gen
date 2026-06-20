import bpy
from .generate_rig import HAIR_RIG_OT_generate, HAIR_RIG_OT_clear
from .generate_from_selection import HAIR_RIG_OT_generate_from_selection

_classes = (
    HAIR_RIG_OT_generate,
    HAIR_RIG_OT_generate_from_selection,
    HAIR_RIG_OT_clear,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
