# ----------------------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the Proprietary License. Please read the https://docs.natsuneko.moe/en-US/limited-license
# ----------------------------------------------------------------------------------------------------------

from __future__ import annotations

import bpy
from bpy.types import Operator
import re

expression = r"^(.*)\.(\w{3})$"

class DuplicateEventListener(Operator):
    bl_idname = "object.duplicate_event_listener"
    bl_label = "Duplicate Event Listener"

    __is_initialized = False
    __listening = False
    __cached_objects = []

    @classmethod
    def is_listening(cls):
        return cls.__listening

    @classmethod
    def reset(cls):
        cls.__listening = False

    def collect_objects(self) -> list[any]:
        objects = bpy.data.objects

        return list(filter(lambda w: True, objects))

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

            if not re.match(expression, obj.name):
                continue

            match = re.search(expression, obj.name)
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

        if not self.is_listening():
            self.__is_initialized = False
            return {'FINISHED'}

        objects = self.collect_objects()

        if not self.__is_initialized:
            self.__cached_objects = objects
            self.__is_initialized = True
            return {'PASS_THROUGH'}

        if len(objects) <= len(self.__cached_objects):
            return {'PASS_THROUGH'}

        newer_objects = self.get_newer_objects(self.__cached_objects, objects)

        self.rename_newer_objects(newer_objects, objects)
        self.__cached_objects = objects

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        cls = DuplicateEventListener

        if context.area.type == "VIEW_3D":
            if not self.is_listening():
                cls.__listening = True
                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}

            else:
                cls.__listening = False
                return {'FINISHED'}

        return {'CANCELED'}