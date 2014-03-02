from __future__ import unicode_literals

from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet
from django.contrib import admin

from . import models


class RequiredInlineFormSet(BaseInlineFormSet):
    NUM_REQUIRED = 2

    """
    XXX: Grrr, I can't get min_num on plain BaseInlineFormSet to work.
         With that, this could be made very general to require based
         on min_num. For the time being this is more specific than we
         can make it when we figure it out.
    """
    def clean(self):
        super(RequiredInlineFormSet, self).clean()
        num_valid = 0

        for form in self.forms:
            if (form.is_valid() and form.has_changed()
                    and not (self.can_delete
                             and form.cleaned_data.get('DELETE'))):
                num_valid += 1

        if num_valid < self.NUM_REQUIRED:
            raise ValidationError("At least {} participants are "
                                  "required.".format(self.NUM_REQUIRED))


class ParticipantInline(admin.TabularInline):
    model = models.Participant
    formset = RequiredInlineFormSet

    def get_extra(self, request, obj=None, **kwargs):
        return 2 if not obj else 0


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]


@admin.register(models.Race)
class RaceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Shot)
class ShotAdmin(admin.ModelAdmin):
    pass
