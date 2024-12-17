from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    """ Модель сотрудника """

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
