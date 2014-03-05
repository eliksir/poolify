# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import choice

from django.db import models
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.translation import ugettext_lazy as _
from quintet.models import TimeStampedModel

from games.models import GameType, Ruleset
from players.models import Player


@python_2_unicode_compatible
class Participant(models.Model):
    """
    Defines a participant in a match.
    """
    TEAM_1 = 0
    TEAM_2 = 1
    TEAM_CHOICES = (
        (TEAM_1, _('Team 1')),
        (TEAM_2, _('Team 2')),
    )

    SUIT_STRIPES = 'Stripes'
    SUIT_SOLIDS = 'Solids'
    SUIT_CHOICES = (
        (SUIT_STRIPES, _('Stripes')),
        (SUIT_SOLIDS, _('Solids')),
    )

    match = models.ForeignKey('Match', verbose_name=_('match'),
            related_name='participants')
    player = models.ForeignKey(Player, verbose_name=_('player'))

    # Will never be stored as blank, but we allow blank selection which will
    # trigger random team assignment.
    team = models.PositiveSmallIntegerField(_('team'), choices=TEAM_CHOICES,
            blank=True)

    suit = models.CharField(_('suit'), max_length=10, choices=SUIT_CHOICES,
            blank=True)

    def __str__(self):
        return "{}: {}".format(self.get_team_display(), self.player)

    class Meta:
        unique_together = ('match', 'player')

    def save(self, *args, **kwargs):
        "Overridden save() to pick team when not designated."
        if not self.team:
            self._pick_team()
        super(Participant, self).save(*args, **kwargs)

    def _pick_team(self):
        "Pick a team based on the teams currently assigned in the match."
        teams = self.match.get_teams()
        t1_size, t2_size = len(teams[0]), len(teams[1])

        if t1_size > t2_size:
            self.team = self.TEAM_2
        elif t1_size < t2_size:
            self.team = self.TEAM_1
        else:
            self.team = choice(self.TEAM_CHOICES)[0]


@python_2_unicode_compatible
class Match(TimeStampedModel):
    """
    Defines a match of a given game with a specific ruleset.
    """
    game_type = models.ForeignKey(GameType, verbose_name=_('game type'))
    ruleset = models.ForeignKey(Ruleset, verbose_name=_('rules'))
    lag_winner = models.ForeignKey(Player, verbose_name=_('winner of the lag'),
            related_name='lag_winners', null=True, blank=True)
    num_races = models.PositiveSmallIntegerField(_('number of races'), default=3)
    players = models.ManyToManyField(Player, through='Participant',
            related_name='matches')

    def __str__(self):
        def names(participants):
            return (x.player.get_full_name() for x in participants)
        teams = self.get_teams()
        return "{} vs. {}".format(", ".join(names(teams[0])),
                                  ", ".join(names(teams[1])))

    class Meta:
        verbose_name_plural = _('matches')

    def get_teams(self):
        "Return a tuple of two lists with participants in the teams."
        participants = self.participants.all()
        return ([x for x in participants if x.team == Participant.TEAM_1],
                [x for x in participants if x.team == Participant.TEAM_2])


@python_2_unicode_compatible
class Race(models.Model):
    """
    Defines a race within a match.
    """
    match = models.ForeignKey(Match, verbose_name=_('match'),
            related_name='races')
    number = models.PositiveSmallIntegerField(_('race number'))

    def __str__(self):
        return "{}: Race {}".format(smart_text(self.match), self.number)

    class Meta:
        get_latest_by = 'number'
        unique_together = ('match', 'number')


@python_2_unicode_compatible
class Outcome(models.Model):
    """
    Defines a potential or actual shot outcome: A ball in a pocket.
    """
    POCKET_FOOT_LEFT = 'F-L'
    POCKET_FOOT_RIGHT = 'F-R'
    POCKET_SIDE_LEFT = 'S-L'
    POCKET_SIDE_RIGHT = 'S-R'
    POCKET_HEAD_LEFT = 'H-L'
    POCKET_HEAD_RIGHT = 'H-R'

    POCKETS = (
        (POCKET_FOOT_LEFT, '\u2196'),
        (POCKET_FOOT_RIGHT, '\u2197'),
        (POCKET_SIDE_LEFT, '\u2190'),
        (POCKET_SIDE_RIGHT, '\u2192'),
        (POCKET_HEAD_LEFT, '\u2199'),
        (POCKET_HEAD_RIGHT, '\u2198'),
    )

    shot = models.ForeignKey('Shot', verbose_name=_('shot'),
            related_name='outcomes', blank=True, null=True,
            help_text=_("Only use this for actual outcomes, NOT called!"))
    ball = models.PositiveSmallIntegerField(_('ball'), blank=True,
            null=True, choices=zip(range(1, 16), range(1, 16)))
    pocket = models.CharField(_('pocket'), max_length=3, blank=True,
            choices=POCKETS)

    def __str__(self):
        return "{} in {}".format(self.ball, self.get_pocket_display())

    class Meta:
        pass

@python_2_unicode_compatible
class Shot(models.Model):
    """
    Defines a shot within a race.
    """
    race = models.ForeignKey(Race, verbose_name=_('race'),
            related_name='shots', related_query_name='shot')
    player = models.ForeignKey(Player, verbose_name=_('player'),
            related_name='shots', related_query_name='shot')
    call = models.OneToOneField(Outcome, verbose_name=_('called shot'),
            related_name='called_shot')
    number = models.PositiveSmallIntegerField(_('shot number'))
    is_legal = models.BooleanField(_('is legally pocketed'), default=None)
    is_foul = models.BooleanField(_('is foul'), default=None)

    def __str__(self):
        return "Shot {}".format(self.number)

    class Meta:
        get_latest_by = 'number'
        unique_together = ('race', 'number')
