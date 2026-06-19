import bpy
from bpy.types import Operator
from mathutils import Vector

from ..core import segmentation, centerline, armature_builder

_MIN_FACES = 3


class HAIR_RIG_OT_generate(Operator):
    bl_idname = "hair_rig.generate"
    bl_label = "Generate Structural Rig"
    bl_description = "Segment the target mesh by hard edges and generate a guide armature"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        settings = context.scene.hair_rig_settings
        return (
            settings.target_object is not None
            and settings.target_object.type == 'MESH'
        )

    def execute(self, context):
        settings = context.scene.hair_rig_settings
        mesh_obj = settings.target_object
        threshold = settings.angle_threshold
        spacing = settings.bone_spacing

        segments = segmentation.segment_mesh(mesh_obj, threshold)
        segments = [s for s in segments if len(s) >= _MIN_FACES]

        if not segments:
            self.report(
                {'WARNING'},
                "No segments found. Try lowering the Angle Threshold.",
            )
            return {'CANCELLED'}

        bb = mesh_obj.bound_box
        world_mat = mesh_obj.matrix_world
        bb_world = [world_mat @ Vector(corner) for corner in bb]
        mesh_centroid = sum(bb_world, Vector()) / 8.0

        chains = []
        for faces in segments:
            p0, p1 = centerline.compute_centerline(faces)
            if (p0 - mesh_centroid).length > (p1 - mesh_centroid).length:
                p0, p1 = p1, p0
            points = centerline.sample_centerline(p0, p1, spacing)
            if len(points) >= 2:
                chains.append(points)

        if not chains:
            self.report({'WARNING'}, "Could not compute any bone chains.")
            return {'CANCELLED'}

        armature_builder.build_armature(context, mesh_obj, chains)

        self.report({'INFO'}, f"Generated armature with {len(chains)} chain(s) from {len(segments)} segment(s).")
        return {'FINISHED'}


class HAIR_RIG_OT_clear(Operator):
    bl_idname = "hair_rig.clear"
    bl_label = "Clear Structural Rig"
    bl_description = "Remove the previously generated Hair_Armature objects from the scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = armature_builder.clear_generated_armatures(context)
        if count:
            self.report({'INFO'}, f"Removed {count} generated armature(s).")
        else:
            self.report({'INFO'}, "No generated armatures found.")
        return {'FINISHED'}
