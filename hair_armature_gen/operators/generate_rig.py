import bpy
from bpy.types import Operator

from ..core import segmentation, centerline, armature_builder

_MIN_VERTS = 3


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
        bones_per_chain = settings.bones_per_chain
        max_chains = settings.max_chains
        min_sep = settings.min_chain_separation

        segments = segmentation.segment_mesh(mesh_obj, threshold)
        segments = [s for s in segments if len(s) >= _MIN_VERTS]

        if not segments:
            self.report(
                {'WARNING'},
                "No segments found. Try lowering the Angle Threshold.",
            )
            return {'CANCELLED'}

        chains = []
        for verts in segments:
            p0, p1 = centerline.compute_centerline(verts)
            # Ensure chains run top-to-bottom so bone tails face downward.
            if p0.z < p1.z:
                p0, p1 = p1, p0
            points = centerline.sample_centerline(p0, p1, bones_per_chain)
            points = centerline.snap_to_vertices(points, verts)
            if len(points) >= 2 and (points[0] - points[-1]).length > 1e-6:
                chains.append(points)

        # Cull chains whose midpoints are too close to an already-accepted chain.
        if min_sep > 0.0:
            accepted_midpoints = []
            filtered = []
            for points in chains:
                mid = points[len(points) // 2]
                if all((mid - m).length >= min_sep for m in accepted_midpoints):
                    accepted_midpoints.append(mid)
                    filtered.append(points)
            chains = filtered

        # Cap total chain count (segments are already sorted largest-first).
        if max_chains > 0:
            chains = chains[:max_chains]

        if not chains:
            self.report({'WARNING'}, "Could not compute any bone chains.")
            return {'CANCELLED'}

        active = context.view_layer.objects.active
        if settings.merge_into_active and active and active.type == 'ARMATURE':
            armature_builder.merge_chains_into_armature(context, active, mesh_obj, chains)
            self.report(
                {'INFO'},
                f"Added {len(chains)} chain(s) to '{active.name}' from {len(segments)} segment(s).",
            )
        else:
            armature_builder.build_armature(context, mesh_obj, chains)
            self.report(
                {'INFO'},
                f"Generated armature with {len(chains)} chain(s) from {len(segments)} segment(s).",
            )
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
