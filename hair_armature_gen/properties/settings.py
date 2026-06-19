import bpy
from bpy.props import FloatProperty, PointerProperty
from bpy.types import PropertyGroup
import math


def _poll_mesh(self, obj):
    return obj.type == 'MESH'


class HairRigSettings(PropertyGroup):
    target_object: PointerProperty(
        name="Target Object",
        type=bpy.types.Object,
        poll=_poll_mesh,
    )

    angle_threshold: FloatProperty(
        name="Angle Threshold",
        description="Minimum dihedral angle between adjacent faces to count as a segment boundary",
        default=math.radians(30.0),
        min=math.radians(1.0),
        max=math.radians(179.0),
        unit='ROTATION',
        subtype='ANGLE',
    )

    bone_spacing: FloatProperty(
        name="Bone Spacing",
        description="Distance between consecutive bones along each centerline",
        default=0.05,
        min=0.001,
        unit='LENGTH',
    )
