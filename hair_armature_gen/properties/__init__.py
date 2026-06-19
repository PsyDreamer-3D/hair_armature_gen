import bpy
from .settings import HairRigSettings

_classes = (HairRigSettings,)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.hair_rig_settings = bpy.props.PointerProperty(type=HairRigSettings)


def unregister():
    del bpy.types.Scene.hair_rig_settings
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
