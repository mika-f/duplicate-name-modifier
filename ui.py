# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

import bpy
from bpy.types import Panel

from .operator import DuplicateEventListener
from .properties import DuplicateNameModifierProperties

class DuplicateEventListenerUI(Panel):
    bl_idname = "UI_PT_DuplicateEventListener"
    bl_label = "Duplicate Naming Style"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Duplicate Naming Style"

    def draw(self, context):
        props: DuplicateNameModifierProperties = context.scene.DuplicateNameModifierProperties

        layout = self.layout

        column = layout.column()
        column.prop(props, "is_listening")

