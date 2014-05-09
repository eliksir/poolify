# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_shot'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(through='matches.Participant', to='players.Player'),
            preserve_default=True,
        ),
    ]
