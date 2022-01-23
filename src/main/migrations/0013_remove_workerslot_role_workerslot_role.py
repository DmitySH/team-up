# Generated by Django 4.0.1 on 2022-01-23 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_profile_belbin_profile_belbin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workerslot',
            name='role',
        ),
        migrations.AddField(
            model_name='workerslot',
            name='role',
            field=models.ManyToManyField(null=True, related_name='worker_slots', to='main.BelbinTest', verbose_name='Роли по Белбину'),
        ),
    ]