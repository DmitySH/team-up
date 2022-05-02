# Generated by Django 4.0.1 on 2022-05-02 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_specialization_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='executoroffer',
            options={'ordering': ['id'], 'verbose_name': 'Карточка работника', 'verbose_name_plural': 'Карточки работника'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='profile_photos/empty.png', null=True, upload_to='profile_photos/', verbose_name='Фотография'),
        ),
    ]
