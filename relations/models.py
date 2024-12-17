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
    name = models.CharField(max_length=150, verbose_name='Название')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,
                                null=True, blank=True,
                                verbose_name='Контакты')
    supplier = models.ForeignKey("self", on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name='Поставщик')
    debt = models.DecimalField(max_digits=20, decimal_places=2, default=0,
                               verbose_name='Задолженность')
    create_at = models.DateTimeField(auto_now_add=True,
                                     verbose_name='Время создания')
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
