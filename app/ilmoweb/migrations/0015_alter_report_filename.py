# Generated by Django 4.2.5 on 2023-10-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0014_alter_report_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='filename',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
