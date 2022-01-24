# Generated by Django 4.0.1 on 2022-01-24 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_profile_remote_alter_project_offline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='remote',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Не указывать'), (1, 'Онлайн'), (2, 'И онлайн, и оффлайн'), (3, 'Оффлайн')], null=True, verbose_name='Удаленная работа'),
        ),
    ]
