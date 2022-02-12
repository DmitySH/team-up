# Generated by Django 4.0.1 on 2022-01-19 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_alter_profile_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='belbintest',
            name='role',
            field=models.CharField(max_length=30,
                                   verbose_name='Роль по Белбину'),
        ),
        migrations.AlterField(
            model_name='lsqtest',
            name='role',
            field=models.CharField(max_length=30,
                                   verbose_name='Роль по Хони-Мамфорду'),
        ),
        migrations.AlterField(
            model_name='mbtitest',
            name='role',
            field=models.CharField(max_length=30,
                                   verbose_name='Роль по Майерсу-Бриггсу'),
        ),
    ]
