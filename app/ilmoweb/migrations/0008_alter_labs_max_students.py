# Generated by Django 4.2.5 on 2023-10-13 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0007_labs_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labs',
            name='max_students',
            field=models.IntegerField(default=1),
        ),
    ]
