import bpy
from bpy.props import FloatProperty, IntProperty, PointerProperty
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

    max_chains: IntProperty(
        name="Max Chains",
        description="Maximum number of bone chains to generate (0 = no limit, largest segments first)",
        default=0,
        min=0,
    )

    min_chain_separation: FloatProperty(
        name="Min Separation",
        description="Minimum distance between chain midpoints; chains closer than this are culled (0 = disabled)",
        default=0.0,
        min=0.0,
        unit='LENGTH',
    )

    bones_per_chain: IntProperty(
        name="Bones Per Chain",
        description="Number of bones in each generated chain",
        default=4,
        min=1,
    )
