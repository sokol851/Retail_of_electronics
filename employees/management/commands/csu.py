from django.core.management import BaseCommand

from employees.models import Employee


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Создаём администратора, если не создан"""
        if not Employee.objects.filter(username="admin"):
            employee = Employee.objects.create(
                username="admin",
                first_name="Admin",
                last_name="Adminov",
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )

            employee.set_password("12345")
            employee.save()
            print('Создан администратор "admin"')
        else:
            print("Админ уже существует!")
