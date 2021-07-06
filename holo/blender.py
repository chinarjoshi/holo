import bpy

for window in bpy.context.window_manager.windows:
    print(window.screen)
    # screen = window.screen

    # for area in screen.areas:
    #     if area.type == 'VIEW_3D':
    #         override = {'window': window, 'screen': screen, 'area': area}
    #         bpy.ops.screen.screen_full_area(override)
    #             break

class Window(bpy.types.Window):
    pass


def register():
    bpy.utils.register_class(Window)

def unregister():
    bpy.utils.unregister_class(Window)


if __name__ == "__main__":
    register()
