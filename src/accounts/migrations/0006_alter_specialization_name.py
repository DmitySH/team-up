# Generated by Django 4.0.1 on 2022-04-24 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profileprojectstatus_worker_slot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Специализация'),
        ),
    ]
