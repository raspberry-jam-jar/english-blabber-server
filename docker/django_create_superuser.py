#!/usr/local/bin/python3

import os
import django

django.setup()

from django.contrib.auth import get_user_model


username = os.environ['SUPERUSER_NAME']
email = os.environ['SUPERUSER_EMAIL']
password = os.environ['SUPERUSER_PASSWORD']

User = get_user_model()
try:
    admin = User.objects.get(username=username)
except User.DoesNotExist:
    admin = User.objects.create(
        username=username, email=email,
        is_staff=True, is_superuser=True
    )
admin.set_password(password)
admin.save()
