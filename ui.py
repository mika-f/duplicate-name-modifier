# ----------------------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the Proprietary License. Please read the https://docs.natsuneko.moe/en-US/limited-license
# ----------------------------------------------------------------------------------------------------------

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
        cls = DuplicateEventListener
        props: DuplicateNameModifierProperties = context.scene.DuplicateNameModifierProperties

        layout = self.layout

        column = layout.column()
        column.prop(props, "is_listening")

