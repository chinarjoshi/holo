# this vector changes the view distance for each screen.area, which should remain constant and only changes by a scale factor from the camera scale
bpy.data.window_managers[0].windows[1].screen.areas[0].spaces[0].region_3d.view_location = Vector((1.4, 1, 1))


import bpy
from bpy.app.handlers import persistent


"""

Steps: # TODO Order steps
 1. remove gui elements and make background black
 2. offset each camera rotation view to make it square
 3. change initial view_distance to match maximum view potential
 4. rotate each camera view with view_rotation.rotate() to make it 90 degree offsets with 45 degree offsets
with respect to the y axis

 5. From there each rotation from the view rotation changes objects[].rotation_euler

"""


bpy.context.window = bpy.data.window_manager[0].windows[-1]


def set_scene(screen_data: SpaceView3D = bpy.data.window_managers[0].windows[-1].screen.areas[0].spaces[0]) -> None:
    screen_data.shading.background_type = 'VIEWPORT'
    screen_data.shading.background_color = (0, 0, 0)
    screen_data.show_gizmo = False
    screen_data.overlay.show_overlays = False
    screen_data.show_region_toolbar = False
    screen_data.show_region_tool_header = False

for view in bpy.data.window_managers[0].windows[-1].screen.areas[0].spaces[0].region_quadviews:



bpy.data.window_managers[0].windows[1].screen.areas[0].spaces[0].region_3d.view_rotation.rotate(Euler((1, 10, .1)))

# ok for now assume that there is a fullscreened quad view on window index 1

bpy.data.window_managers[0].windows[1].screen.areas[0].spaces[0].region_3d.view_distance

for window in bpy.data.window_managers[0].windows: # let's find what's what
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            if len(area.spaces[0].region_quadviews) > 0: #if quadviews are active
                quad_views = area.spaces[0].region_quadviews
            else:
                main_view = area.spaces[0].region_3d

@persistent # This makes it stay if another file is opened
def update_handler(dummy):
    for every_view in quad_views:
        every_view.view_location = main_view.view_location
        every_view.view_distance = main_view.view_distance

    [area for area in bpy.data.window_managers[0].windows[0].screen.areas if area.type == 'VIEW_3D'][0]



bpy.app.handlers.frame_change_post.append(update_handler)
#bpy.app.handlers.scene_update_post.remove(update_handler)
