from rest_framework import serializers

from relations.models import Contact, Partner, Product


class ProductSerializer(serializers.ModelSerializer):
    release_date = serializers.DateField(format="%d.%m.%Y")
    partner_id = serializers.PrimaryKeyRelatedField(
        queryset=Partner.objects.all(),
        write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date', 'partner_id']

    def create(self, validated_data):
        # Достаём id партнёра
        partner = validated_data.pop('partner_id', None)
        # Создаём продукт
        product = Product.objects.create(**validated_data)
        # Связываем продукт с партнером
        if partner:
            partner.products.add(product)
        return product


class ProductForPartnerSerializer(serializers.ModelSerializer):
    release_date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(required=False)
    products = ProductForPartnerSerializer(many=True,
                                           required=False)
    create_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M",
                                          required=False,
                                          read_only=True)

    class Meta:
        model = Partner
        fields = "__all__"
        extra_kwargs = {'debt': {'read_only': True}}

    def validate_supplier(self, supplier):
        # Проверяем, чтобы у завода не было поставщика
        # Проверка при создании
        if self.initial_data.get('type_organization') == 0:
            raise serializers.ValidationError({
                'supplier': "У завода не может быть поставщика."
            })
        # Проверка при обновлении
        if self.instance:
            if self.instance.type_organization == 0:
                raise serializers.ValidationError({
                    'supplier': "У завода не может быть поставщика."
                })

        # Проверяем, что партнёр не может быть себе поставщиком.
        if self.instance:
            if supplier.id == self.instance.id:
                raise serializers.ValidationError({
                    "supplier": "Партнёр не может быть себе поставщиком."})
        return supplier

    @staticmethod
    def validate_contact(contact):
        # Проверяем, что контакт принадлежит только одному партнёру.
        if Contact.objects.filter(**contact).exists():
            raise serializers.ValidationError({
                'contact': "Контакт уже связан с другим поставщиком."
            })
        return contact

    def create(self, validated_data):
        # Собираем данные с ввода
        try:
            contact_data = validated_data.pop('contact')
        except Exception:
            raise serializers.ValidationError(
                {'Не указаны контакты в формате': {'contact': {
                    'email': 'None',
                    'country': 'None',
                    'city': 'None',
                    'street': 'None',
                    'house_number': 'None'}
                }})
        try:
            products_data = validated_data.pop('products')
            if not products_data:
                raise serializers.ValidationError(
                    'Список продуктов не может быть пустым')
        except Exception:
            raise serializers.ValidationError(
                {'Не указаны продукты в формате': {'products': [
                    {'name': 'Product1',
                     'model': 'v.1',
                     'release_date':
                         '2024-01-01'},
                    {'name': 'Product2',
                     'model': 'v.2',
                     'release_date':
                         '2023-12-30'}]
                }})

        # Добавляем объект контакта
        contact = Contact.objects.create(**contact_data)

        # Создаём объект партнёра
        partner = Partner.objects.create(**validated_data,
                                         contact=contact)

        # Добавляем объекты продуктов
        for product_data in products_data:
            # Создаем или получаем продукт
            product, _ = Product.objects.get_or_create(**product_data)
            partner.products.add(product)  # добавляем продукт к партнёру
        return partner

    def update(self, instance, validated_data):
        # Собираем данные с ввода
        contact_data = validated_data.pop('contact', None)
        products_data = validated_data.pop('products', None)

        # Изменяем объект контакта
        if contact_data:
            contact = instance.contact
            for key, value in contact_data.items():
                setattr(instance.contact, key, value)
            contact.save()

        # Изменяем объект партнёра
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Обрабатываем продукты
        if products_data:
            # Сохраним текущие продукты
            current_products = list(instance.products.all())
            # Очищаем текущие продукты
            instance.products.clear()

            for product_data in products_data:
                product, _ = Product.objects.update_or_create(
                    id=product_data.get('id', None),
                    defaults=product_data
                )
                # Добавляем продукт к Partner
                instance.products.add(product)

            for product in current_products:
                # Проверяем, связан ли продукт с другими партнерами
                if not product.partner_set.exists():
                    # Удаляем, если продукт остался без связи
                    product.delete()

        instance.save()  # Сохраняем изменения
        return instance
