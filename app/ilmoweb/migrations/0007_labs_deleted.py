# Generated by Django 4.2.5 on 2023-10-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0006_remove_labs_minim_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='labs',
            name='deleted',
            field=models.BooleanField(default=0),
        ),
    ]
