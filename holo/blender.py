import bpy
import json
from bpy.types import SpaceView3D
from bpy.app.handlers import persistent
from mathutils import Quaternion, Matrix, Vector


def duplicate_window(window_type: str = 'INVOKE_DEFAULT') -> None:
    """Duplicates a new window into bpy.data.screens from current active window."""
    context_window = bpy.context.copy()
    context_window['area'] = [area for area in bpy.context.screen.areas if area.type == 'VIEW_3D'][0]
    bpy.ops.screen.area_dupli(context_window, window_type)


def convert_quadview(area: SpaceView3D) -> None:
    """Converts a given window into quad-view."""
    region = [region for region in RENDER_AREA.regions if region.type == 'WINDOW'][0]
    override = {'area': RENDER_AREA, 'region': region, 'edit_object': bpy.context.edit_object}
    bpy.ops.screen.region_quadview(override)


def configure_scene(screen_data: SpaceView3D) -> None:
    """Removes all overlay elements from the 3D viewport."""
    screen_data.shading.background_type = 'VIEWPORT'
    screen_data.shading.background_color = (0, 0, 0)
    screen_data.overlay.show_overlays = False
    for attribute in 'show_gizmo', 'show_region_toolbar', 'show_region_tool_header':
        setattr(screen_data, attribute, False)


def initial_config(values: list) -> None:
    for index, window in enumerate(values):
        for key, attribute in window.items():
            if key not in {'perspective_matrix', 'window_matrix'}:
                setattr(QUAD_VIEWS[index], key, attribute)


if __name__ == '__main__':
    duplicate_window()
    RENDER_AREA = bpy.data.window_managers[0].windows[-1].screen.areas[0]
    MAIN_VIEW = [area for area in bpy.data.window_managers[0].windows[0].screen.areas if area.type == 'VIEW_3D'][0].spaces[0].region_3d
    QUAD_VIEWS = RENDER_AREA.spaces[0].region_quadviews
    convert_quadview(area=RENDER_AREA)
    configure_scene(screen_data=RENDER_AREA.spaces[0])
    initial_config(values=[
        {
            "perspective_matrix": Matrix(((0.38953691720962524, -0.9948844313621521, 0.8873997926712036, 1.274999737739563),
            (0.180816650390625, 1.67820405960083, 1.8021012544631958, -0.2884082496166229),
            (0.957085371017456, 0.15791277587413788, -0.24308671057224274, 5.14061975479126),
                                        (0.9570661783218384, 0.15790961682796478, -0.24308183789253235, 5.160516262054443))),
            "view_distance": 4,
            "view_location": Vector((-1.1843680143356323, 0.5826243758201599, -0.2636926770210266)),
            "view_matrix": Matrix(((0.28046655654907227, -0.7163167595863342, 0.6389278173446655, 0.917999804019928),
            (0.07323073595762253, 0.6796725988388062, 0.7298509478569031, -0.11680532991886139),
            (-0.9570661783218384, -0.15790961682796478, 0.24308183789253235, -5.160516262054443),
                                (0.0, 0.0, 0.0, 1.0))),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((0.7421625256538391, 0.2990451455116272, -0.5376160740852356, -0.26596173644065857)),
            "window_matrix": Matrix(((1.388888955116272, 0.0, 0.0, 0.0),
            (0.0, 2.4691359996795654, 0.0, 0.0),
            (0.0, 0.0, -1.0000200271606445, -0.02000020071864128),
            (0.0, 0.0, -1.0, 0.0)))
        },
        {
            "perspective_matrix": Matrix(((1.0067499876022339, -0.15708249807357788, 0.9438177943229675, 1.390674114227295),
            (1.6992019414901733, 0.4048176407814026, -1.745126724243164, -0.6900960206985474),
            (0.03147741034626961, -0.9799830913543701, -0.19667792320251465, 5.288571357727051),
                                        (0.03147678077220917, -0.979963481426239, -0.19667398929595947, 5.308465003967285))),
            "view_distance": 4,
            "view_location": Vector((-0.6476320624351501, 3.713759183883667, -0.16454876959323883)),
            "view_matrix": Matrix(((0.7248599529266357, -0.11309938877820969, 0.6795487999916077, 1.0012853145599365),
            (0.6881767511367798, 0.16395112872123718, -0.7067762613296509, -0.27948886156082153),
            (-0.03147678077220917, 0.979963481426239, 0.19667398929595947, -5.308465003967285),
                                (0.0, 0.0, 0.0, 1.0))),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((-0.7220604419708252, 0.5840023756027222, 0.24617943167686462, 0.2774270176887512)),
            "window_matrix": Matrix(((1.388888955116272, 0.0, 0.0, 0.0),
            (0.0, 2.4691359996795654, 0.0, 0.0),
            (0.0, 0.0, -1.0000200271606445, -0.02000020071864128),
                                    (0.0, 0.0, -1.0, 0.0))),
        },
        {
            "perspective_matrix": Matrix(((0.6381685137748718, -0.27682116627693176, -1.202133059501648, -1.501191258430481),
            (2.1930031776428223, 0.23790904879570007, 1.109400987625122, 0.00046116337762214243),
            (0.006154918111860752, 0.9752073884010315, -0.22129832208156586, 6.274174213409424),
                                        (0.0061547947116196156, 0.9751878380775452, -0.22129389643669128, 6.294048309326172))),
            "view_distance": 4,
            "view_location": Vector((0.494803786277771, -0.47912198305130005, -0.8757699131965637)),
            "view_matrix": Matrix(((0.45948129892349243, -0.19931122660636902, -0.8655357360839844, -1.0808576345443726),
            (0.8881661891937256, 0.09635315835475922, 0.4493073523044586, 0.00018677115440368652),
            (-0.0061547947116196156, -0.9751878380775452, 0.22129389643669128, -6.294048309326172),
                                (0.0, 0.0, 0.0, 1.0))),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((0.6665449142456055, 0.5342831611633301, 0.32232666015625, -0.40787842869758606)),
            "window_matrix": Matrix(((1.388888955116272, 0.0, 0.0, 0.0),
            (0.0, 2.4691359996795654, 0.0, 0.0),
            (0.0, 0.0, -1.0000200271606445, -0.02000020071864128),
                                    (0.0, 0.0, -1.0, 0.0))),
        },
        {
            "perspective_matrix": Matrix(((0.3718714416027069, -0.8294840455055237, -1.0500859022140503, -1.3293282985687256),
            (-0.1070108637213707, 1.917167067527771, -1.5523052215576172, 0.10223301500082016),
            (-0.962533175945282, -0.2010997086763382, -0.18201333284378052, 4.386408805847168),
                                        (-0.9625139236450195, -0.20109568536281586, -0.18200968205928802, 4.406320571899414))),
            "view_distance": 4,
            "view_location": Vector((-1.2986540794372559, -0.9290060997009277, -0.9919807314872742)),
            "view_matrix": Matrix(((0.2677474319934845, -0.597228467464447, -0.7560617923736572, -0.9571163654327393),
            (-0.04333939775824547, 0.7764526009559631, -0.6286835670471191, 0.0414043664932251),
            (0.9625139236450195, 0.20109568536281586, 0.18200968205928802, -4.406320571899414),
                                (0.0, 0.0, 0.0, 1.0))),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((0.7460244297981262, -0.27806705236434937, 0.5759113430976868, -0.18561358749866486)),
            "window_matrix": Matrix(((1.388888955116272, 0.0, 0.0, 0.0),
            (0.0, 2.4691359996795654, 0.0, 0.0),
            (0.0, 0.0, -1.0000200271606445, -0.02000020071864128),
            (0.0, 0.0, -1.0, 0.0)))
        }
    ])



# bpy.data.window_managers[0].windows[1].screen.areas[0].spaces[0].region_3d.view_rotation.rotate(Euler((1, 10, .1)))

for window in bpy.data.window_managers[0].windows: # let's find what's what
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            if len(area.spaces[0].region_quadviews) > 0: #if quadviews are active
                quad_views = area.spaces[0].region_quadviews
            else:
                main_view = area.spaces[0].region_3d

@persistent # This makes it stay if another file is opened
def update_handler(dummy):
    for every_view in QUAD_VIEWS:
        every_view.view_location = MAIN_VIEW.view_location
        every_view.view_distance = MAIN_VIEW.view_distance

bpy.app.handlers.frame_change_post.append(update_handler)
