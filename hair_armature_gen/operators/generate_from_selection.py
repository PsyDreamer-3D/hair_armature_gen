import bpy
from bpy.types import Operator

from ..core import selection, armature_builder


class HAIR_RIG_OT_generate_from_selection(Operator):
    bl_idname = "hair_rig.generate_from_selection"
    bl_label = "Generate Chain from Selection"
    bl_description = (
        "Create bone chains from the vertices selected on the target mesh. "
        "Select vertices in Edit Mode, return to Object Mode, then click this button."
    )
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
        bones_per_chain = settings.bones_per_chain

        islands = selection.get_selected_islands(mesh_obj)
        if not islands:
            self.report({'WARNING'}, "No vertices selected on the target mesh.")
            return {'CANCELLED'}

        chains = []
        for indices in islands:
            ordered = selection.order_island_by_path(indices, mesh_obj)
            if len(ordered) < 2:
                continue
            resampled = selection.resample_polyline(ordered, bones_per_chain)
            if len(resampled) < 2 or (resampled[0] - resampled[-1]).length < 1e-6:
                continue
            # Ensure root-to-tip runs top-to-bottom (same convention as auto-generate)
            if resampled[0].z < resampled[-1].z:
                resampled.reverse()
            chains.append(resampled)

        if not chains:
            self.report({'WARNING'}, "Could not build any bone chains from the selection.")
            return {'CANCELLED'}

        active = context.view_layer.objects.active
        if settings.merge_into_active and active and active.type == 'ARMATURE':
            armature_builder.merge_chains_into_armature(context, active, mesh_obj, chains)
            self.report(
                {'INFO'},
                f"Added {len(chains)} chain(s) to '{active.name}' from {len(islands)} selected island(s).",
            )
        else:
            armature_builder.build_armature(context, mesh_obj, chains)
            self.report(
                {'INFO'},
                f"Generated armature with {len(chains)} chain(s) from {len(islands)} selected island(s).",
            )
        return {'FINISHED'}
