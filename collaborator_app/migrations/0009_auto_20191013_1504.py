# Generated by Django 2.2.3 on 2019-10-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborator_app', '0008_auto_20191013_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolistitem',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
