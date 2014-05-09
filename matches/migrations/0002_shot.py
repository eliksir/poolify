# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '__first__'),
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('race', models.ForeignKey(verbose_name='race', to_field='id', to='matches.Race')),
                ('player', models.ForeignKey(verbose_name='player', to_field='id', to='players.Player')),
                ('call', models.OneToOneField(to_field='id', verbose_name='called shot', to='matches.Outcome')),
                ('number', models.PositiveSmallIntegerField(verbose_name='shot number')),
                ('is_legal', models.BooleanField(verbose_name='is legally pocketed', default=None)),
                ('is_foul', models.BooleanField(verbose_name='is foul', default=None)),
            ],
            options={
                'get_latest_by': 'number',
                'unique_together': set([('race', 'number')]),
            },
            bases=(models.Model,),
        ),
    ]
