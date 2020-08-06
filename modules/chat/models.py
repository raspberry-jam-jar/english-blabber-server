from django.db import models

from class_room.models import LearningGroup, User


class Message(models.Model):
    datetime_created = models.DateTimeField(auto_now=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='messages', )
    chatroom = models.ForeignKey(LearningGroup, on_delete=models.CASCADE,
                                 related_name='messages', )
