# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

import bpy

from bpy.props import BoolProperty
from bpy.types import PropertyGroup

class DuplicateNameModifierProperties(PropertyGroup):

    def on_update(self, context):
        bpy.ops.object.duplicate_event_listener("INVOKE_DEFAULT")

    is_listening: BoolProperty(name = "Apply Underscore-style Naming Convention", default=False, update=on_update, options={"HIDDEN"})