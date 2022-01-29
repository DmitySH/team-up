from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, \
    MaxValueValidator
from django.db import models
from django.urls import reverse

from src.tests.models import BelbinTest, MBTITest, LSQTest
from django.utils.translation import gettext_lazy as _


class Specialization(models.Model):
    """
    Специализация.
    """

    name = models.CharField('Специализация', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Profile(models.Model):
    """
    Пользователь сайта (расширение модели user).
    """

    class RemoteChoices(models.IntegerChoices):
        __empty__ = _('Не указывать')
        ONLINE = 1, _('Онлайн')
        ONLINE_AND_OFFLINE = 2, _('И онлайн, и оффлайн')
        OFFLINE = 3, _('Оффлайн')

    def get_remote_value(self):
        return self.RemoteChoices.choices[self.remote][1]

    # Sex choices codes:
    MALE = True
    FEMALE = False

    SEX_CHOICES = (
        (None, 'Не указывать'),
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile'
                                )

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.user:
            print('sdfsdfsdf')
            self.user.delete()

    patronymic = models.CharField('Отчество', max_length=30, blank=True,
                                  default='', null=True)
    photo = models.ImageField('Фотография', upload_to='profile_photos/',
                              default='profile_photos/empty.png',
                              blank=True)
    description = models.TextField('Описание',
                                   default='Пользователь не рассказывает о себе',
                                   blank=True
                                   )
    cv = models.FileField('Резюме', upload_to='cvs', null=True, blank=True,
                          validators=[
                              FileExtensionValidator(['pdf', 'docx', 'doc'])])

    belbin = models.ManyToManyField(BelbinTest,
                                    verbose_name='Результат теста по Белбину',
                                    related_name='profiles',
                                    blank=True
                                    )
    mbti = models.ManyToManyField(MBTITest,
                                  verbose_name='Результат теста Майерса-Бриггса',
                                  related_name='profiles',
                                  blank=True
                                  )
    lsq = models.ManyToManyField(LSQTest,
                                 verbose_name='Результат теста Хони-Мамфорда',
                                 related_name='profiles',
                                 blank=True
                                 )

    remote = models.PositiveSmallIntegerField(
        'Удаленная работа',
        choices=RemoteChoices.choices,
        blank=True,
        null=True
    )

    is_male = models.BooleanField('Пол',
                                  choices=SEX_CHOICES,
                                  default=None,
                                  null=True,
                                  blank=True)
    specialization = models.ManyToManyField(Specialization,
                                            verbose_name='Специализация',
                                            blank=True
                                            )
    city = models.CharField('Город', max_length=50, blank=True)
    age = models.PositiveSmallIntegerField('Возраст',
                                           validators=[
                                               MinValueValidator(14),
                                               MaxValueValidator(100)
                                           ],
                                           null=True,
                                           blank=True
                                           )
    verified = models.BooleanField('Подтвержден', default=False)

    def __str__(self):
        return '{surname} {name} {second_name}' \
            .format(surname=self.user.last_name,
                    name=self.user.first_name,
                    second_name=self.patronymic
                    )

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.user.username})

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
