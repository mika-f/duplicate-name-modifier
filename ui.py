# ----------------------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the Proprietary License. Please read the https://docs.natsuneko.moe/en-US/limited-license
# ----------------------------------------------------------------------------------------------------------

from bpy.types import Panel

from .operator import DuplicateEventListener


class DuplicateEventListenerUI(Panel):
    bl_idname = "UI_PT_DuplicateEventListener"
    bl_label = "Listener"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Duplicate Event Listener"

    def draw(self, context):
        cls = DuplicateEventListener
        layout = self.layout

        if not cls.is_listening():
            layout.operator(cls.bl_idname, text="Start Listening", icon="PLAY")
        else:
            layout.operator(cls.bl_idname, text="Stop Listening", icon="PAUSE")
