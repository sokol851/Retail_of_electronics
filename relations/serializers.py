from psycopg2 import IntegrityError
from rest_framework import serializers

from relations.models import Contact, Partner, Product


class ProductSerializer(serializers.ModelSerializer):
    release_date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = Product
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True)
    create_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M",
                                          required=False)

    class Meta:
        model = Partner
        fields = "__all__"
        extra_kwargs = {'debt': {'read_only': True}}

    def validate(self, attrs):
        type_organization = attrs.get('type_organization')
        supplier = attrs.get('supplier')
        # Проверяем тип организации и указание поле поставщика
        if type_organization == 0 and supplier is not None:
            raise serializers.ValidationError({
                'supplier': "У завода не может быть поставщика."
            })

        return attrs

    def create(self, validated_data):
        # Собираем данные с ввода
        contact_data = validated_data.pop('contact')
        products_data = validated_data.pop('products')

        # Добавляем объект контакта
        contact = Contact.objects.create(**contact_data)

        # Создаём объект партнёра
        partner = Partner.objects.create(**validated_data, contact=contact)

        # Добавляем объекты продуктов
        for product_data in products_data:
            product = Product.objects.create(**product_data)  # создаем продукт
            partner.products.add(product)  # добавляем продукт к партнёру

        return partner

    def update(self, instance, validated_data):
        # Собираем данные с ввода
        contact_data = validated_data.pop('contact')
        products_data = validated_data.pop('products', None)

        # Изменяем объект контакта
        if contact_data:
            # Находим текущий contact и обновляем его с использованием kwargs
            contact = instance.contact
            for key, value in contact_data.items():
                setattr(contact, key, value)
            contact.save()

        # Изменяем объект партнёра
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Обрабатываем продукты
        if products_data is not None:
            # Обновляем связанный список продуктов
            current_products = list(instance.products.all())  # Сохраним текущие продукты
            instance.products.clear()  # Очищаем текущие продукты, если необходимо


            for product_data in products_data:
                product, created = Product.objects.update_or_create(
                    id=product_data.get('id', None),  # Если у вас есть id продукта
                    defaults=product_data
                )
                instance.products.add(product)  # Добавляем продукт к Partner

            for product in current_products:
                if not product.partner_set.exists():  # Проверяем, связан ли продукт с другими партнерами
                    product.delete()

        instance.save()  # Сохраняем изменения в Partner
        return instance
