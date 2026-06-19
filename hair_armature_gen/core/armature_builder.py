import bpy
from mathutils import Vector


_GENERATED_PREFIX = "Hair_Armature"


def build_armature(context, mesh_obj, chains, name=_GENERATED_PREFIX):
    """Create and return a new armature object containing Bone_ROOT and one chain per entry in *chains*.

    *chains* is a list of lists of mathutils.Vector (world-space positions),
    ordered root-to-tip.  Each inner list must have at least 2 points.

    Bone creation requires armature Edit Mode.  The armature object is
    temporarily made active for the mode switch, then restored.
    """
    arm_data = bpy.data.armatures.new(name)
    arm_obj = bpy.data.objects.new(name, arm_data)
    context.collection.objects.link(arm_obj)

    prev_active = context.view_layer.objects.active
    arm_obj.select_set(True)
    context.view_layer.objects.active = arm_obj

    with context.temp_override(
        active_object=arm_obj,
        object=arm_obj,
        selected_objects=[arm_obj],
        selectable_objects=[arm_obj],
    ):
        bpy.ops.object.mode_set(mode='EDIT')

        edit_bones = arm_data.edit_bones

        bb = mesh_obj.bound_box
        world_mat = mesh_obj.matrix_world
        bb_world = [world_mat @ Vector(corner) for corner in bb]
        centroid = sum(bb_world, Vector()) / 8.0

        root_eb = edit_bones.new("Bone_ROOT")
        root_eb.head = centroid
        root_eb.tail = centroid + Vector((0.0, 0.0, 0.05))

        for chain_idx, points in enumerate(chains):
            prev_eb = None
            for bone_idx in range(len(points) - 1):
                eb = edit_bones.new(f"Hair_{chain_idx:03d}_{bone_idx:03d}")
                eb.head = points[bone_idx]
                eb.tail = points[bone_idx + 1]
                if prev_eb is None:
                    eb.parent = root_eb
                    eb.use_connect = False
                else:
                    eb.parent = prev_eb
                    eb.use_connect = True
                prev_eb = eb

        root_eb = None
        prev_eb = None

        bpy.ops.object.mode_set(mode='OBJECT')

    context.view_layer.objects.active = prev_active
    return arm_obj


def clear_generated_armatures(context):
    """Remove all armature objects whose name starts with the generated prefix."""
    to_remove = [
        obj for obj in context.scene.objects
        if obj.type == 'ARMATURE' and obj.name.startswith(_GENERATED_PREFIX)
    ]
    for obj in to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)
    return len(to_remove)
