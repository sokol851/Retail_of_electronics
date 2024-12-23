from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee
from relations.models import Contact, Partner, Product
from relations.serializers import (PartnerSerializer,
                                   ProductForPartnerSerializer,
                                   ProductSerializer)


class PartnerAdminTests(TestCase):
    """ Тестирование админ-панели партнёра """

    def setUp(self):
        # Создаём админа
        self.user = Employee.objects.create_superuser(
            username='adm',
            email='admin@example.com',
            password='password123',
            is_active=True,
            is_superuser=True,
            is_staff=True
        )

        # Авторизуем его
        self.client.login(username='adm', password='password123')

        # Создаём контакты
        self.contact = Contact.objects.create(email='i@i.ru',
                                              country='Россия',
                                              city='СПб',
                                              street='Ленина',
                                              house_number='10')
        self.contact2 = Contact.objects.create(email='a@a.ru',
                                               country='Россия',
                                               city='СПб',
                                               street='Ленина',
                                               house_number='10')

        # Создаём продукт
        self.product = Product.objects.create(name='Стул',
                                              model='Деревянный',
                                              release_date='2024-01-01')

        # Создаём партнёра 1
        self.partner = Partner.objects.create(
            name='Партнёр',
            type_organization=0,
            contact=self.contact,
            debt=100.10
        )
        self.partner2 = Partner.objects.create(
            name='Партнёр2',
            type_organization=1,
            contact=self.contact2,
            supplier=self.partner,
            debt=0.0
        )
        self.partner.products.add(self.product)

    def test_partner_admin_list_display(self):
        self.assertEqual(self.product.__str__(), 'Стул')
        # Проверяем, что параметры list_display отображаются на странице
        response = self.client.get(reverse('admin:'
                                           'relations_partner_changelist'))
        self.assertContains(response, 'Партнёр')
        self.assertContains(response, 'Завод')
        self.assertContains(response, 'СПб')
        self.assertContains(response, 'i@i.ru (Россия)')
        self.assertContains(response, "100,10")

    def test_delete_partner(self):
        # Проверяем удаление объекта
        self.partner.delete()
        partner = Partner.objects.filter(name='Партнёр').exists()
        self.assertFalse(partner)


class PartnerModelTests(TestCase):
    def setUp(self):
        # Создаем контакт
        self.contact = Contact.objects.create(email='i@i.ru',
                                              country='Россия',
                                              city='СПб',
                                              street='Ленина',
                                              house_number='10')

        # Создаём продукт
        self.product = Product.objects.create(name='Стул',
                                              model='Деревянный',
                                              release_date='2024-01-01')

    def test_clean_self_supplier(self):
        # Проверяем, является ли поставщиком для себя
        partner = Partner(name='Партнёр',
                          type_organization=0,
                          contact=self.contact)
        # Устанавливаем поставщика себя же
        partner.supplier = partner
        with self.assertRaises(ValidationError):
            partner.clean()

    def test_clean_factory_has_supplier(self):
        # Проверяем, что завод не имеет поставщика
        partner = Partner(name='Завод',
                          type_organization=0,
                          contact=self.contact)
        # Устанавливаем поставщика
        partner.supplier = Partner(name='Поставщик',
                                   type_organization=1,
                                   contact=self.contact)
        with self.assertRaises(ValidationError):
            partner.clean()

    def test_clean_duplicate_name(self):
        # Проверяем, на уникальность названия
        Partner.objects.create(name='Партнёр',
                               type_organization=1,
                               contact=self.contact)
        partner_2 = Partner(name='Партнёр',
                            type_organization=1,
                            contact=self.contact)
        with self.assertRaises(ValidationError):
            partner_2.clean()

    def test_clean_success(self):
        # Проверяем успешную валидацию
        partner = Partner(name='Партнёр',
                          type_organization=1,
                          contact=self.contact)
        partner.clean()


class PartnerTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые объекты Partner и Contact
        self.contact = Contact.objects.create(email='i@i.ru',
                                              country='Россия',
                                              city='СПб',
                                              street='Ленина',
                                              house_number='10')

        self.partner = Partner.objects.create(name='Партнёр',
                                              type_organization=1,
                                              contact=self.contact)

    def test_create_product_success(self):
        # Проверяем успешное создание продукта
        data = {
            'name': 'Продукт',
            'model': '1',
            'release_date': '2024-01-01',
            'partner_id': self.partner.pk
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()

        # Проверяем, что продукт создан
        self.assertEqual(product.name, 'Продукт')
        self.assertEqual(product.model, '1')
        self.assertEqual(product.release_date.strftime("%d.%m.%Y"),
                         '01.01.2024')

        # Проверяем, что продукт связан с партнером
        self.assertIn(product, self.partner.products.all())

    def test_create_product_without_partner(self):
        # Проверяем создание продукта без указания партнёра
        data = {
            'name': 'Продукт2',
            'model': '2',
            'release_date': '2024-02-02'
        }
        serializer = ProductForPartnerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()

        # Проверяем, что продукт создан
        self.assertEqual(product.name, 'Продукт2')
        self.assertEqual(product.model, '2')
        self.assertEqual(product.release_date.strftime("%d.%m.%Y"),
                         '02.02.2024')

        # Проверяем, что продукт не связан с партнёром
        self.assertNotIn(product, self.partner.products.all())

    def test_create_product_invalid_data(self):
        # Проверяем не верный ввод
        data = {
            'name': '',  # Имя пустое
            'model': '3',
            'release_date': '2024-03-03',
            'partner_id': self.partner.pk
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # Проверяем, что ошибка связана с полем name
        self.assertIn('name', serializer.errors)

    def test_create_product_invalid_date_format(self):
        # Проверяем создание продукта с недействительным форматом даты
        data = {
            'name': 'Продукт3',
            'model': '3',
            'release_date': '2024_01_01',  # Неправильный формат даты
            'partner_id': self.partner.pk
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # Проверяем, что ошибка связана с полем release_date
        self.assertIn('release_date', serializer.errors)


class PartnerSerializerTests(TestCase):

    def setUp(self):
        # Создаем тестовые объекты Contact и Product
        self.partner = {
            'name': 'Партнёр',
            'type_organization': 0,
            'products': [{'name': 'Стул',
                          'model': 'Деревянный',
                          'release_date': '2024-01-01'
                          }],
            'contact': {'email': 'i@i.ru',
                        'country': 'Россия',
                        'city': 'СПб',
                        'street': 'Ленина',
                        'house_number': '10'
                        },
            'debt': 0.00
        }

        self.contact2 = Contact.objects.create(email='a@a.ru',
                                               country='Россия',
                                               city='СПб',
                                               street='Ленина',
                                               house_number='10')
        self.partner2 = Partner.objects.create(name='Партнёр2',
                                               type_organization=1,
                                               contact=self.contact2)

        self.product2 = Product.objects.create(name='Стул',
                                               model='Деревянный',
                                               release_date='2024-01-01')
        self.partner2.products.add(self.product2)

        self.serializer = PartnerSerializer(data=self.partner)

    def test_create_partner_success(self):
        # Проверяем успешное создание партнёра
        self.assertTrue(self.serializer.is_valid())
        partner = self.serializer.save()

        # Проверяем, что партнёр создан
        self.assertEqual(partner.name, 'Партнёр')
        self.assertEqual(partner.contact.email, 'i@i.ru')

    def test_create_validators(self):
        # Устанавливаем поставщика для завода
        self.partner['supplier'] = self.partner2.pk
        # Устанавливаем чужие контакты
        self.partner['contact'] = {'email': 'a@a.ru',
                                   'country': 'Россия',
                                   'city': 'СПб',
                                   'street': 'Ленина',
                                   'house_number': '10'
                                   }

        serializer = PartnerSerializer(data=self.partner)
        self.assertFalse(serializer.is_valid())
        self.assertIn('supplier', serializer.errors)
        self.assertIn('contact', serializer.errors)

        # Проверяем отсутствие поставщика у завода
        self.assertEqual(serializer.errors['supplier'], {
            'supplier': "У завода не может быть поставщика."
        })
        # Проверяем уникальность соответствия контактов
        self.assertEqual(serializer.errors['contact'], {
            'contact': "Контакт уже связан с другим поставщиком."
        })

    def test_update_partner_success(self):
        # Данные для обновления
        self.assertTrue(self.serializer.is_valid())
        partner = self.serializer.save()

        update_data = {
            'name': 'Партнёр_upd',
            'type_organization': 1,
            'products': [{'name': 'Стол',
                          'model': 'Светлый',
                          'release_date': '2024-01-05'
                          }],
            'contact': {'email': 'u@u.ru',
                        'country': 'РФ',
                        'city': 'МСК',
                        'street': 'Свободы',
                        'house_number': '11'
                        },
            'supplier': partner.pk,
            'debt': 0.00
        }

        # Обновляем партнёра
        serializer = PartnerSerializer(instance=self.partner2,
                                       data=update_data)
        self.assertTrue(serializer.is_valid())
        updated_partner = serializer.save()

        # Проверяем, что данные обновлены
        self.assertEqual(updated_partner.name, 'Партнёр_upd')
        self.assertEqual(updated_partner.contact.email, 'u@u.ru')

        # Проверяем, что продукты добавлены
        self.assertEqual(updated_partner.products.count(), 1)

    def test_update_supplier_fail(self):
        # Данные для обновления
        update_data = {
            'name': 'Партнёр2',
            'type_organization': 1,
            'supplier': self.partner2.pk
        }

        serializer = PartnerSerializer(instance=self.partner2,
                                       data=update_data)
        self.assertFalse(serializer.is_valid())

        self.assertIn('supplier', serializer.errors)

        self.assertEqual(serializer.errors['supplier'], {
            "supplier": "Партнёр не может быть себе поставщиком."})
