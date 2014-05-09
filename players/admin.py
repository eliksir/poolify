from django.contrib import admin

from players import models


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
