# Generated by Django 5.0.4 on 2024-12-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_game_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='genre',
            field=models.TextField(default='empty', max_length=255),
        ),
    ]
