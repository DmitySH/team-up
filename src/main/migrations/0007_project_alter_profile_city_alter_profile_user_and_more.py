# Generated by Django 4.0.1 on 2022-01-19 11:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_alter_belbintest_role_alter_lsqtest_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('vacant', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)], verbose_name='Вакантных мест')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='Город')),
                ('remote', models.CharField(blank=True, choices=[('Требуется присутствие', 'Требуется присутствие'), ('Присутствие не требуется', 'Присутствие не требуется')], default='', max_length=40, verbose_name='Требуется работать не удаленно')),
                ('verified', models.BooleanField(default=False, verbose_name='Подтвержден')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=50, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='WorkerSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Описание')),
                ('salary', models.PositiveIntegerField(blank=True, null=True, verbose_name='Зарплата')),
                ('work_hours', models.PositiveSmallIntegerField(default=40, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(168)], verbose_name='Часы работы в неделю')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_slots', to='main.profile', verbose_name='Профиль работника')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='worker_slots', to='main.belbintest', verbose_name='Роли по Белбину')),
                ('specialization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.specialization', verbose_name='Специализация')),
            ],
            options={
                'verbose_name': 'Слот работника',
                'verbose_name_plural': 'Слоты работника',
            },
        ),
        migrations.CreateModel(
            name='ExecutorOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Описание')),
                ('salary', models.PositiveIntegerField(blank=True, null=True, verbose_name='Зарплата')),
                ('work_hours', models.PositiveSmallIntegerField(default=40, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(168)], verbose_name='Часы работы в неделю')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='executor_offer', to='main.profile')),
            ],
            options={
                'verbose_name': 'Карточка работника',
                'verbose_name_plural': 'Карточки работника',
            },
        ),
    ]
