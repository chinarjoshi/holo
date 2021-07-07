import bpy
from bpy.app.handlers import persistent


context = bpy.context.copy()

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        context['area'] = area

        if len(area.spaces[0].region_quadviews) > 0:
            quad_views = area.spaces[0].region_quadviews
        else:
            main_view = area.spaces[0].region_3d





for w in bpy.data.window_managers[0].windows: # let's find what's what
    for a in w.screen.areas:
        if a.type == 'VIEW_3D':
            if len(a.spaces[0].region_quadviews) > 0: #if quadviews are active
                quad_views = a.spaces[0].region_quadviews
            else:
                main_view = a.spaces[0].region_3d

@persistent # This makes it stay if another file is opened
def update_handler(dummy):
    for every_view in quad_views:
        every_view.view_location = main_view.view_location
        every_view.view_distance = main_view.view_distance



bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')


# bpy.app.handlers.scene_update_post.append(update_handler)
#bpy.app.handlers.scene_update_post.remove(update_handler)
