# Generated by Django 4.2.7 on 2023-11-29 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0024_rename_filename_report_report_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeachersMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
            ],
        ),
    ]
