# Generated by Django 4.0.1 on 2022-01-18 19:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main',
         '0002_remove_profile_name_remove_profile_second_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BelbinTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('role', models.CharField(max_length=20,
                                          verbose_name='Роль по Белбину')),
            ],
            options={
                'verbose_name': 'Роль по Белбину',
                'verbose_name_plural': 'Роли по Белбину',
            },
        ),
        migrations.CreateModel(
            name='LSQTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('role', models.CharField(max_length=20,
                                          verbose_name='Роль по Хони-Мамфорду')),
            ],
            options={
                'verbose_name': 'Роль по Хони-Мамфорду',
                'verbose_name_plural': 'Роли по Хони-Мамфорду',
            },
        ),
        migrations.CreateModel(
            name='MBTITest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('role', models.CharField(max_length=20,
                                          verbose_name='Роль по Майерсу-Бриггсу')),
            ],
            options={
                'verbose_name': 'Роль по Майерсу-Бриггсу',
                'verbose_name_plural': 'Роли по Майерсу-Бриггсу',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=50,
                                          verbose_name='Специализация')),
            ],
            options={
                'verbose_name': 'Специализация',
                'verbose_name_plural': 'Специализации',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True,
                                                   validators=[
                                                       django.core.validators.MinValueValidator(
                                                           14),
                                                       django.core.validators.MaxValueValidator(
                                                           100)],
                                                   verbose_name='Возраст'),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=30,
                                   verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='profile',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='cvs',
                                   verbose_name='Резюме'),
        ),
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True,
                                   default='Пользователь не рассказывает о себе',
                                   verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_male',
            field=models.BooleanField(blank=True, default=None, null=True,
                                      verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/',
                                    verbose_name='Фотография'),
        ),
        migrations.AddField(
            model_name='profile',
            name='remote',
            field=models.CharField(choices=[('Предпочитаю удаленную работу',
                                             'Предпочитаю удаленную работу'), (
                                                'Предпочитаю работу в офисе',
                                                'Предпочитаю работу в офисе'),
                                            (
                                                'Могу работать как онлайн, так и оффлайн',
                                                'Могу работать как онлайн, так и оффлайн')],
                                   default='', max_length=40,
                                   verbose_name='Возможность работать не удаленно'),
        ),
        migrations.AddField(
            model_name='profile',
            name='verified',
            field=models.BooleanField(default=False,
                                      verbose_name='Подтвержден'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='patronymic',
            field=models.CharField(blank=True, max_length=30,
                                   verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='profile',
            name='belbin',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='profiles',
                                    to='main.belbintest',
                                    verbose_name='Результат теста по Белбину'),
        ),
        migrations.AddField(
            model_name='profile',
            name='lsq',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='profiles', to='main.lsqtest',
                                    verbose_name='Результат теста Хони-Мамфорда'),
        ),
        migrations.AddField(
            model_name='profile',
            name='mbti',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='profiles',
                                    to='main.mbtitest',
                                    verbose_name='Результат теста Майерса-Бриггса'),
        ),
        migrations.AddField(
            model_name='profile',
            name='specialization',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='main.specialization',
                                    verbose_name='Специализация'),
        ),
    ]
