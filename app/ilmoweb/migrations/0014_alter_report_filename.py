# Generated by Django 4.2.5 on 2023-10-17 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0013_alter_report_filename_alter_report_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='filename',
            field=models.FileField(null=True, upload_to='upload/'),
        ),
    ]
