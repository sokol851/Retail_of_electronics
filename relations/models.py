from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Contact(models.Model):
    email = models.EmailField(verbose_name='Почта')
    country = models.CharField(max_length=75, verbose_name='Страна')
    city = models.CharField(max_length=75, verbose_name='Город')
    street = models.CharField(max_length=75, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')

    def __str__(self):
        return f'{self.email} ({self.country})'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    model = models.CharField(max_length=75, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выпуска')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Partner(models.Model):
    TYPE_ORGANIZATIONS = {0: 'Завод',
                          1: 'Розничная сеть',
                          2: 'ИП'}

    name = models.CharField(max_length=150,
                            unique=True,
                            verbose_name='Название')
    type_organization = models.IntegerField(choices=TYPE_ORGANIZATIONS,
                                            verbose_name='Тип организации')
    contact = models.OneToOneField(Contact, on_delete=models.PROTECT,
                                   verbose_name='Контакты')
    supplier = models.ForeignKey("self",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name='Поставщик')
    debt = models.DecimalField(max_digits=20,
                               decimal_places=2,
                               default=0,
                               validators=[MinValueValidator(Decimal('0.00'))],
                               verbose_name='Задолженность')
    create_at = models.DateTimeField(auto_now_add=True,
                                     verbose_name='Время создания')
    products = models.ManyToManyField(Product, verbose_name='Продукты')

    def clean(self):
        if self.supplier == self:
            raise ValidationError(
                'Партнёр не может быть поставщиком для себя.')
        if self.type_organization == 0 and self.supplier is not None:
            raise ValidationError(
                "У завода не может быть поставщика.")
        # Валидация при создании
        if self.pk is None:
            if Partner.objects.filter(name=self.name).exists():
                raise ValidationError(
                    "Партнёр с таким названием уже зарегистрирован.")

    def __str__(self):
        return f'{self.name} - {self.contact.city}'

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
        ordering = ('name',)
