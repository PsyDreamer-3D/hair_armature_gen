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

        col = layout.column(align=True)
        col.prop(settings, "angle_threshold")
        col.prop(settings, "bone_spacing")

        layout.separator()
        layout.operator("hair_rig.generate", icon='ARMATURE_DATA')
        layout.operator("hair_rig.clear", icon='TRASH')
