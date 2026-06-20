import bpy
from bpy.types import Panel


class HAIR_RIG_PT_main(Panel):
    bl_label = "Hair Rig"
    bl_idname = "HAIR_RIG_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Hair Rig"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.hair_rig_settings

        layout.prop(settings, "target_object")

        layout.separator()
        layout.label(text="Segmentation")
        layout.prop(settings, "angle_threshold")

        layout.separator()
        layout.label(text="Chain Density")
        col = layout.column(align=True)
        col.prop(settings, "max_chains")
        col.prop(settings, "min_chain_separation")

        layout.separator()
        layout.label(text="Bones")
        layout.prop(settings, "bones_per_chain")

        layout.separator()
        layout.label(text="Output")
        row = layout.row()
        row.prop(settings, "merge_into_active")
        active = context.view_layer.objects.active
        if settings.merge_into_active and (not active or active.type != 'ARMATURE'):
            row.label(text="No armature active", icon='ERROR')

        layout.separator()
        layout.operator("hair_rig.generate", icon='ARMATURE_DATA')
        layout.operator("hair_rig.generate_from_selection", icon='RESTRICT_SELECT_OFF')
        layout.operator("hair_rig.clear", icon='TRASH')
