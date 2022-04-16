from django.db import models


class BelbinTest(models.Model):
    """
    Belbin role db model.
    """

    role = models.CharField('Роль по Белбину', max_length=30)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = 'Роль по Белбину'
        verbose_name_plural = 'Роли по Белбину'


class MBTITest(models.Model):
    """
    MBTI role db model.
    """

    role = models.CharField('Роль по Майерсу-Бриггсу', max_length=30)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = 'Роль по Майерсу-Бриггсу'
        verbose_name_plural = 'Роли по Майерсу-Бриггсу'


class LSQTest(models.Model):
    """
    LSQ role db model.
    """

    role = models.CharField('Роль по Хони-Мамфорду', max_length=30)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = 'Роль по Хони-Мамфорду'
        verbose_name_plural = 'Роли по Хони-Мамфорду'
