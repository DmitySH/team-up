from django.db import models


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
