# Generated by Django 4.0.1 on 2022-02-10 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('main', '0024_profileprojectstatus_worker_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileprojectstatus',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='accounts.profile', verbose_name='Владелец'),
        ),
    ]