# Generated by Django 4.0.5 on 2022-07-22 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monito_api', '0005_log_entered_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='moniurl',
            name='failedCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='moniurl',
            name='lastStatus',
            field=models.BooleanField(default=True),
        ),
    ]
