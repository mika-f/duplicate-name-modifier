# ----------------------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the Proprietary License. Please read the https://docs.natsuneko.moe/en-US/limited-license
# ----------------------------------------------------------------------------------------------------------

bl_info = {
    "name": "Duplicate Name Modifier",
    "author": "Natsuneko",
    "description": "Blender add-on for changing naming convention when objects are duplicated",
    "blender": (3, 0, 0),
    "version": (1, 0, 1),
    "location": "3D View > Sidebar > Duplicate Name Modifier",
    "warning": "",
    "category": "Generic"
}

if "bpy" in locals():
    import importlib
    importlib.reload(operator)
    importlib.reload(properties)
    importlib.reload(ui)
else:
    from . import operator
    from . import properties
    from . import ui

    import bpy
    from bpy.props import PointerProperty


classes = [
    operator.DuplicateEventListener,
    properties.DuplicateNameModifierProperties,
    ui.DuplicateEventListenerUI
]


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.DuplicateNameModifierProperties = PointerProperty(type=properties.DuplicateNameModifierProperties)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.DuplicateNameModifierProperties


if __name__ == "__main__":
    register()
