# Generated by Django 4.0.1 on 2022-01-18 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_belbintest_lsqtest_mbtitest_specialization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='belbin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to='main.belbintest', verbose_name='Результат теста по Белбину'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lsq',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to='main.lsqtest', verbose_name='Результат теста Хони-Мамфорда'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mbti',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to='main.mbtitest', verbose_name='Результат теста Майерса-Бриггса'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='remote',
            field=models.CharField(blank=True, choices=[('Предпочитаю удаленную работу', 'Предпочитаю удаленную работу'), ('Предпочитаю работу в офисе', 'Предпочитаю работу в офисе'), ('Могу работать как онлайн, так и оффлайн', 'Могу работать как онлайн, так и оффлайн')], default='', max_length=40, verbose_name='Возможность работать не удаленно'),
        ),
    ]