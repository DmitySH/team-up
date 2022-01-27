# Generated by Django 4.0.1 on 2022-01-24 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_profile_belbin_alter_profile_lsq_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='remote',
        ),
        migrations.AddField(
            model_name='project',
            name='offline',
            field=models.BooleanField(blank=True, choices=[(None, 'Не указывать'), (True, 'Требуется присутствие'), (False, 'Присутствие не требуется')], default=None, null=True, verbose_name='Требуется работать не удаленно'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='remote',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Не указывать'), (1, 'Предпочитаю удаленную работу'), (3, 'Предпочитаю работу в офисе'), (2, 'Могу работать как онлайн, так и оффлайн')], default=None, null=True, verbose_name='Удаленная работа'),
        ),
    ]