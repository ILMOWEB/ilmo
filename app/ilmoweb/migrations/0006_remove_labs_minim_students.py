# Generated by Django 4.2.5 on 2023-10-07 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0005_labgroups_signed_up_students_labs_minim_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labs',
            name='minim_students',
        ),
    ]
