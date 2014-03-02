from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Player(User):

    def __str__(self):
        return self.get_full_name()

    class Meta:
        proxy = True
