from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class GameType(models.Model):
    """
    Defines a game type, such as Eight-ball or Nine-ball.
    """
    name = models.CharField(_('name'), max_length=30)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Ruleset(models.Model):
    """
    Defines a ruleset for a given game type, i.e. WPA rules.
    """
    name = models.CharField(_('name'), max_length=30)
    game_type = models.ForeignKey(GameType, verbose_name=_('game type'),
            related_name='rulesets', related_query_name='ruleset')
    rules_text = models.TextField(_('rules text'))

    def __str__(self):
        return "{}: {}".format(self.game_type.name, self.name)
