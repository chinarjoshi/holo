#!/usr/bin/env python3

import bpy

class HoloPanel(bpy.types.Panel):
    """Create shaders for your Poser figure: Panel"""
    bl_label = "Figure Files Info"
    bl_idname = "MATERIALS_PT_shaders"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Skin Shaders"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text='Figure Name')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("mesh.primitive_cube_add", text='Find Images', icon='FILESEL')
        row = layout.row()
        row.operator("object.run_script", text = 'Apply Shaders')

class runScript(bpy.types.Operator):
    """Tooltip"""
    # was bl_idname = "object.run_script" - is now:
    bl_idname = "object.run_script"
    bl_label = "Invokes a Script"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print('Yay!')

        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_class(__name__)

if __name__ == "__main__":
    register()
