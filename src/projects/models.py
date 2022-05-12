from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from src.tests.models import BelbinTest


class Project(models.Model):
    """
    Project.
    """

    # Remote choices codes:
    OFFLINE = False
    ONLINE = True

    REMOTE_CHOICES = (
        (None, 'Не указывать'),
        (OFFLINE, 'Требуется присутствие'),
        (ONLINE, 'Присутствие не требуется'),
    )

    @property
    def remote_value(self):
        return self.REMOTE_CHOICES[2][1] if self.online else \
            self.REMOTE_CHOICES[1][1]

    owner = models.ForeignKey(
        'accounts.Profile',
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        related_name='projects',
        null=True
    )

    title = models.CharField('Название', max_length=200, unique=True)
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

    required_specialization = models.ManyToManyField('accounts.Specialization',
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
        ordering = ['-id']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class WorkerSlot(models.Model):
    """
    Card of worker in project.
    """

    profile = models.ForeignKey('accounts.Profile',
                                verbose_name='Профиль работника',
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

    specialization = models.ManyToManyField('accounts.Specialization',
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
        return 'Слот в проекте {project}' \
            .format(project=self.project)

    class Meta:
        verbose_name = 'Слот работника'
        verbose_name_plural = 'Слоты работника'
