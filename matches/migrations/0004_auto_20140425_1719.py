# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_match_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcome',
            name='shot',
            field=models.ForeignKey(help_text='Only use this for actual outcomes, NOT called!', verbose_name='shot', null=True, to='matches.Shot', blank=True, to_field='id'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='outcome',
            unique_together=set([('shot', 'ball')]),
        ),
    ]
