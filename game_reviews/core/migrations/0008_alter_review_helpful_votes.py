# Generated by Django 5.1.3 on 2024-12-14 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_review_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='helpful_votes',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]