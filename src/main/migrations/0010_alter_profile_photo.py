# Generated by Django 4.0.1 on 2022-01-22 18:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main',
         '0009_status_alter_project_options_project_required_belbin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True,
                                    default='profile_photos/empty.png',
                                    upload_to='profile_photos/',
                                    verbose_name='Фотография'),
        ),
    ]
