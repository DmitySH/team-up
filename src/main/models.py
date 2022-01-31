from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from src.accounts.models import Profile, Specialization
from src.tests.models import BelbinTest, MBTITest, LSQTest


class ExecutorOffer(models.Model):
    """
    Предложение работника.
    """

    profile = models.OneToOneField(Profile,
                                   on_delete=models.CASCADE,
                                   related_name='executor_offer'
                                   )
    description = models.TextField('Описание')
    salary = models.PositiveIntegerField('Зарплата', null=True, blank=True)
    work_hours = models.PositiveSmallIntegerField('Часы работы в неделю',
                                                  validators=[
                                                      MinValueValidator(1),
                                                      MaxValueValidator(168)
                                                  ],
                                                  default=40
                                                  )

    def __str__(self):
        return 'Карточка {profile}'.format(profile=self.profile.user.username)

    class Meta:
        verbose_name = 'Карточка работника'
        verbose_name_plural = 'Карточки работника'


class Project(models.Model):
    """
    Проект.
    """

    # Remote choices codes:
    OFFLINE = False
    ONLINE = True

    REMOTE_CHOICES = (
        (None, 'Не указывать'),
        (OFFLINE, 'Требуется присутствие'),
        (ONLINE, 'Присутствие не требуется'),
    )

    def get_remote_value(self):
        return self.REMOTE_CHOICES[2][1] if self.online else \
            self.REMOTE_CHOICES[1][1]

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    vacant = models.PositiveSmallIntegerField('Вакантных мест',
                                              validators=[
                                                  MinValueValidator(1),
                                                  MaxValueValidator(20)
                                              ]
                                              )
    city = models.CharField('Город', max_length=50, blank=True)
    online = models.BooleanField('Возможность работы онлайн',
                                 choices=REMOTE_CHOICES,
                                 default=None,
                                 null=True,
                                 blank=True
                                 )
    verified = models.BooleanField('Подтвержден', default=False)

    required_specialization = models.ManyToManyField(Specialization,
                                                     verbose_name='Требуемые специализации',
                                                     related_name='projects',
                                                     )
    required_belbin = models.ManyToManyField(BelbinTest,
                                             verbose_name='Требуемые роли по Белбину',
                                             related_name='projects',
                                             )

    def __str__(self):
        return 'Проект {project}'.format(project=self.title)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.title})

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class WorkerSlot(models.Model):
    """
    Карточка работника в проекте.
    """

    profile = models.ForeignKey(Profile, verbose_name='Профиль работника',
                                on_delete=models.CASCADE,
                                related_name='worker_slots',
                                null=True,
                                blank=True
                                )
    description = models.TextField('Описание')
    salary = models.PositiveIntegerField('Зарплата', null=True, blank=True)
    work_hours = models.PositiveSmallIntegerField('Часы работы в неделю',
                                                  validators=[
                                                      MinValueValidator(1),
                                                      MaxValueValidator(168)
                                                  ],
                                                  default=40
                                                  )
    role = models.ManyToManyField(BelbinTest,
                                  verbose_name='Роли по Белбину',
                                  related_name='worker_slots',
                                  )

    specialization = models.ManyToManyField(Specialization,
                                            verbose_name='Специализации',
                                            related_name='worker_slots'
                                            )
    project = models.ForeignKey(Project,
                                verbose_name='Проект',
                                on_delete=models.CASCADE,
                                related_name='team',
                                null=True
                                )

    def __str__(self):
        return 'Слот работника {profile}' \
            .format(profile=self.profile.user.username)

    class Meta:
        verbose_name = 'Слот работника'
        verbose_name_plural = 'Слоты работника'


# У кого есть ForeignKey, у того будет РОВНО ОДНА связь. К кому идет - у того
# будет много их.

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


class ProfileProjectStatus(models.Model):
    """
    Статусы для вовлеченных в проект пользователей.
    """

    project = models.ForeignKey(Project,
                                verbose_name='Проект',
                                on_delete=models.CASCADE,
                                related_name='profile_statuses',
                                null=True
                                )
    profile = models.ForeignKey(Profile,
                                verbose_name='Профиль',
                                on_delete=models.CASCADE,
                                related_name='profile_statuses',
                                null=True
                                )
    status = models.ForeignKey(Status,
                               verbose_name='Статус',
                               on_delete=models.SET_NULL,
                               related_name='profile_statuses',
                               null=True
                               )

    def __str__(self):
        return '{username} в проекте {project} имеет статус {status}'.format(
            username=self.profile.user.username,
            project=self.project.title,
            status=self.status.value
        )

    class Meta:
        verbose_name = 'Статус вовлеченных в проект пользователей'
        verbose_name_plural = 'Статусы вовлеченных в проект пользователей'
