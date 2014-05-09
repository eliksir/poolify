# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '__first__'),
        ('games', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('game_type', models.ForeignKey(verbose_name='game type', to_field='id', to='games.GameType')),
                ('ruleset', models.ForeignKey(verbose_name='rules', to_field='id', to='games.Ruleset')),
                ('lag_winner', models.ForeignKey(to_field='id', verbose_name='winner of the lag', null=True, to='players.Player', blank=True)),
                ('num_races', models.PositiveSmallIntegerField(verbose_name='number of races', default=3)),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('match', models.ForeignKey(verbose_name='match', to_field='id', to='matches.Match')),
                ('player', models.ForeignKey(verbose_name='player', to_field='id', to='players.Player')),
                ('team', models.PositiveSmallIntegerField(choices=[(0, 'Team 1'), (1, 'Team 2')], verbose_name='team', blank=True)),
                ('suit', models.CharField(choices=[('Stripes', 'Stripes'), ('Solids', 'Solids')], verbose_name='suit', max_length=10, blank=True)),
            ],
            options={
                'unique_together': set([('match', 'player')]),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('match', models.ForeignKey(verbose_name='match', to_field='id', to='matches.Match')),
                ('number', models.PositiveSmallIntegerField(verbose_name='race number')),
            ],
            options={
                'get_latest_by': 'number',
                'unique_together': set([('match', 'number')]),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('ball', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15)], verbose_name='ball', null=True, blank=True)),
                ('pocket', models.CharField(choices=[('F-L', '↖'), ('F-R', '↗'), ('S-L', '←'), ('S-R', '→'), ('H-L', '↙'), ('H-R', '↘')], verbose_name='pocket', max_length=3, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
