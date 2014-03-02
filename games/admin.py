from __future__ import unicode_literals

from django.contrib import admin

from . import models


@admin.register(models.GameType)
class GameTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Ruleset)
class RulesetAdmin(admin.ModelAdmin):
    pass
