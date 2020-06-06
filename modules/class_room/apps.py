from django.apps import AppConfig


class ClassRoomConfig(AppConfig):
    name = 'class_room'

    def ready(self):
        import class_room.signals  # noqa: F401
