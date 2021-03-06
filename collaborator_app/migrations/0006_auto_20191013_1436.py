# Generated by Django 2.2.3 on 2019-10-13 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborator_app', '0005_auto_20191012_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=10)),
                ('item_name', models.CharField(max_length=20)),
                ('item_description', models.CharField(max_length=20)),
                ('assigned_to', models.CharField(blank=True, max_length=100)),
                ('due', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.CharField(blank=True, default='', max_length=1000000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='projects',
            field=models.CharField(blank=True, default='', max_length=1000000),
        ),
    ]
