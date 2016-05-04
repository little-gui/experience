from __future__ import unicode_literals
import uuid

from django.db import models
from django.contrib.auth.models import User


class Login(models.Model):
	user = models.OneToOneField(User)
	code = models.UUIDField(default=uuid.uuid4)

