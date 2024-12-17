from rest_framework import serializers

from employees.models import Employee


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователей """

    class Meta:
        model = Employee
        fields = "__all__"
