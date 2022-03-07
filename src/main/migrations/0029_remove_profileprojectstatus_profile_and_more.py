# Generated by Django 4.0.1 on 2022-02-12 20:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0028_alter_profileprojectstatus_status_delete_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileprojectstatus',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profileprojectstatus',
            name='status',
        ),
        migrations.RemoveField(
            model_name='profileprojectstatus',
            name='worker_slot',
        ),
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='project',
            name='required_belbin',
        ),
        migrations.RemoveField(
            model_name='project',
            name='required_specialization',
        ),
        migrations.RemoveField(
            model_name='workerslot',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='workerslot',
            name='project',
        ),
        migrations.RemoveField(
            model_name='workerslot',
            name='role',
        ),
        migrations.RemoveField(
            model_name='workerslot',
            name='specialization',
        ),
        migrations.DeleteModel(
            name='ExecutorOffer',
        ),
        migrations.DeleteModel(
            name='ProfileProjectStatus',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='WorkerSlot',
        ),
    ]