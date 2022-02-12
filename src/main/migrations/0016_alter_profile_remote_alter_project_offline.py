# Generated by Django 4.0.1 on 2022-01-24 13:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0015_remove_project_remote_project_offline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='remote',
            field=models.PositiveSmallIntegerField(blank=True, choices=[
                (None, 'Не указывать'), (1, 'Онлайн'), (2, 'Оффлайн'),
                (3, 'Не имеет значения')], null=True,
                                                   verbose_name='Удаленная работа'),
        ),
        migrations.AlterField(
            model_name='project',
            name='offline',
            field=models.BooleanField(blank=True,
                                      choices=[(None, 'Не указывать'),
                                               (True, 'Требуется присутствие'),
                                               (False,
                                                'Присутствие не требуется')],
                                      default=None, null=True,
                                      verbose_name='Возможность работы онлайн'),
        ),
    ]
