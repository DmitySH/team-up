from django.core.validators import MinValueValidator, MaxValueValidator, \
    FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Tests' models.
class BelbinTest(models.Model):
    """
    Роль по Белбину.
    """

    role = models.CharField('Роль по Белбину', max_length=30)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = 'Роль по Белбину'
        verbose_name_plural = 'Роли по Белбину'


class MBTITest(models.Model):
    """
    Роль по Майерсу-Бриггсу.
    """

    role = models.CharField('Роль по Майерсу-Бриггсу', max_length=30)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = 'Роль по Майерсу-Бриггсу'
        verbose_name_plural = 'Роли по Майерсу-Бриггсу'


class LSQTest(models.Model):
    """
    Роль по Хони-Мамфорду.
    """

    role = models.CharField('Роль по Хони-Мамфорду', max_length=30)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = 'Роль по Хони-Мамфорду'
        verbose_name_plural = 'Роли по Хони-Мамфорду'


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

    # Remote choices codes:
    WANTS_WORK_ONLINE = 'Предпочитаю удаленную работу'
    WANTS_WORK_OFFLINE = 'Предпочитаю работу в офисе'
    DOESNT_MATTER = 'Могу работать как онлайн, так и оффлайн'

    REMOTE_CHOICES = (
        (WANTS_WORK_ONLINE, WANTS_WORK_ONLINE),
        (WANTS_WORK_OFFLINE, WANTS_WORK_OFFLINE),
        (DOESNT_MATTER, DOESNT_MATTER),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile'
                                )

    patronymic = models.CharField('Отчество', max_length=30, blank=True)
    photo = models.ImageField('Фотография', upload_to='profile_photos/',
                              default='profile_photos/empty.png',
                              blank=True)
    description = models.TextField('Описание',
                                   default='Пользователь не рассказывает о себе',
                                   blank=True
                                   )
    cv = models.FileField('Резюме', upload_to='cvs', null=True, blank=True,
                          validators=[FileExtensionValidator(['pdf', 'docx'])])

    belbin = models.ForeignKey(BelbinTest,
                               verbose_name='Результат теста по Белбину',
                               on_delete=models.SET_NULL,
                               related_name='profiles',
                               null=True,
                               blank=True
                               )
    mbti = models.ForeignKey(MBTITest,
                             verbose_name='Результат теста Майерса-Бриггса',
                             on_delete=models.SET_NULL,
                             related_name='profiles',
                             null=True,
                             blank=True
                             )
    lsq = models.ForeignKey(LSQTest,
                            verbose_name='Результат теста Хони-Мамфорда',
                            on_delete=models.SET_NULL,
                            related_name='profiles',
                            null=True,
                            blank=True
                            )

    remote = models.CharField('Возможность работать не удаленно',
                              choices=REMOTE_CHOICES,
                              max_length=40,
                              default='',
                              blank=True
                              )
    is_male = models.BooleanField('Пол', default=None, null=True, blank=True)
    specialization = models.ForeignKey(Specialization,
                                       verbose_name='Специализация',
                                       on_delete=models.SET_NULL,
                                       null=True,
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
        return reverse('user_detail', kwargs={'slug': self.user.username})

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ExecutorOffer(models.Model):
    """
    Предложение работника.
    """

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,
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
    ONLINE = 'Требуется присутствие'
    OFFLINE = 'Присутствие не требуется'

    REMOTE_CHOICES = (
        (ONLINE, ONLINE),
        (OFFLINE, OFFLINE),
    )

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    vacant = models.PositiveSmallIntegerField('Вакантных мест',
                                              validators=[
                                                  MinValueValidator(1),
                                                  MaxValueValidator(20)
                                              ]
                                              )
    city = models.CharField('Город', max_length=50, blank=True)
    remote = models.CharField('Требуется работать не удаленно',
                              choices=REMOTE_CHOICES,
                              max_length=40,
                              default='',
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

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class WorkerSlot(models.Model):
    """
    Карточка работника в проекте.
    """

    profile = models.ForeignKey(Profile, verbose_name='Профиль работника',
                                on_delete=models.CASCADE,
                                related_name='worker_slots'
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
    role = models.ForeignKey(BelbinTest,
                             verbose_name='Роли по Белбину',
                             on_delete=models.SET_NULL,
                             related_name='worker_slots',
                             null=True
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
