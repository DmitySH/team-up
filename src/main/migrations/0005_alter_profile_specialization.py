# Generated by Django 4.0.1 on 2022-01-18 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0004_alter_profile_belbin_alter_profile_lsq_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='specialization',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='main.specialization',
                                    verbose_name='Специализация'),
        ),
    ]
