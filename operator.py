# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

from __future__ import annotations

import bpy
from bpy.types import Operator
import re

from .properties import DuplicateNameModifierProperties

expression1 = r"^(.*)\.(\w{3})$"
expression2 = r"^(.*)_(\w{3})$"

class DuplicateEventListener(Operator):
    bl_idname = "object.duplicate_event_listener"
    bl_label = "Duplicate Event Listener"

    __is_initialized = False
    __cached_objects = []

    def collect_objects(self) -> list[any]:
        objects = bpy.data.objects

        return list(filter(lambda w: hasattr(w, "name"), objects))

    def get_newer_objects(self, old_objects: list[any], new_objects: list[any]) -> list[any]:
        news = []

        for obj in new_objects:
            if obj in old_objects:
                continue
            news.append(obj)

        return news

    def has_same_name_object(self, name: str, objects: list[any]) -> bool:
        for obj in objects:
            if not hasattr(obj, "name"):
                continue

            if obj.name == name:
                return True
        return False

    def rename_newer_objects(self, objects: list[any], existing_objects: list[any]) -> None:
        for obj in objects:
            if not hasattr(obj, "name"):
                continue

            if not re.match(expression1, obj.name):
                continue

            match = re.search(expression1, obj.name)

            # when Object.001 copied, destination object is named as Object.002
            # when Object_001 copied, destination object is named as Object_002
            if re.match(expression2, match.group(1)):
                match = re.search(expression2, match.group(1))

                counter = int(1)
            else:
                counter = int(match.group(2))

            while True:
                new_name = match.group(1) + "_" + str(counter).zfill(3)

                if self.has_same_name_object(new_name, existing_objects):
                    counter += 1
                    continue

                obj.name = new_name
                break

        return

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if not context.scene.DuplicateNameModifierProperties.is_listening:
            self.__is_initialized = False
            return {'FINISHED'}

        objects = self.collect_objects()

        if not self.__is_initialized:
            self.__cached_objects = objects
            self.__is_initialized = True
            return {'PASS_THROUGH'}

        if len(objects) <= len(self.__cached_objects):
            self.__cached_objects = objects
            return {'PASS_THROUGH'}

        newer_objects = self.get_newer_objects(self.__cached_objects, objects)

        self.rename_newer_objects(newer_objects, objects)
        self.__cached_objects = objects

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        cls = DuplicateEventListener
        props: DuplicateNameModifierProperties = context.scene.DuplicateNameModifierProperties


        if context.area.type == "VIEW_3D":
            if props.is_listening:
                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}

            else:
                return {'FINISHED'}

        return {'CANCELED'}