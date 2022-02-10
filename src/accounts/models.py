from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
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


class Status(models.Model):
    """
    Статусы пользователей в проекте.
    """

    value = models.CharField('Статус в проекте', max_length=20)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Статус в проекте'
        verbose_name_plural = 'Статусы в проекте'


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
        return '({username}) {surname} {name} {second_name}' \
            .format(surname=self.user.last_name,
                    name=self.user.first_name,
                    second_name=self.patronymic,
                    username=self.user.username
                    )

    def offer(self):
        try:
            return self.executor_offer
        except ObjectDoesNotExist:
            return None

    def project(self):
        try:
            return self.projects.first()
        except ObjectDoesNotExist:
            return None

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.user.username})

    def get_invited_slots(self):
        invitations = self.profile_statuses.filter(
            status=Status.objects.get(value='Приглашен'))
        slots = [relation.worker_slot for relation in invitations]
        return slots

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
