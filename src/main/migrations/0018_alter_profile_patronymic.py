# Generated by Django 4.0.1 on 2022-01-24 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0017_alter_profile_remote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='patronymic',
            field=models.CharField(blank=True, default='', max_length=30,
                                   verbose_name='Отчество'),
        ),
    ]
