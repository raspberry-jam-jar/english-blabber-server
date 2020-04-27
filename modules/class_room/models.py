import os

from django.contrib.auth.models import User as DefaultUser
from django.db import models


ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student')
)


class User(DefaultUser):
    role = models.CharField(choices=ROLE_CHOICES, max_length=250)
    date_of_birth = models.DateField(
        help_text='Set the date in the format YYYY-MM-DD or select the date.'
    )
    image = models.ImageField(
        upload_to='users/%Y/%m/%d/', null=True, blank=True
    )

    learning_group = models.ForeignKey(
        'LearningGroup', on_delete=models.SET_NULL, related_name='users',
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.get_full_name()} {self.role}'

    def delete(self, **kwargs):
        path = self.image.path
        deletion_info = super().delete(**kwargs)

        os.remove(path)

        return deletion_info


class LearningGroup(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description[:50]


class SocialUser(models.Model):
    code = models.CharField(
        max_length=150, verbose_name='User id at social platform'
    )
    platform = models.CharField(max_length=150, default='vk')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    datetime_created = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='social_users', null=True
    )

    @property
    def status(self):
        return 'pending' if not self.user else 'user'

    class Meta:
        unique_together = [['code', 'platform']]
