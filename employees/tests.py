from django.core import management
from django.test import TestCase

from employees.models import Employee


class EmployeeTestCase(TestCase):
    """ Тесты для приложения персонала """

    def test_csu(self):
        # Удаляем админа
        Employee.objects.filter(username="admin").delete()
        # Проверяем его отсутствие
        self.assertFalse(Employee.objects.filter(username="admin").exists())
        # Запускаем команду
        management.call_command("csu")
        # Проверяем создание
        self.assertTrue(Employee.objects.filter(username="admin").exists())
        # Запускаем снова команду
        result = management.call_command("csu")
        # Проверяем отсутствие результата
        self.assertIsNone(result)
        # Проверяем метод __str__ модели
        admin = Employee.objects.get(username="admin")
        self.assertEqual(admin.__str__(), 'admin')
