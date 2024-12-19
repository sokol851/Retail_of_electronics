from rest_framework import serializers

from relations.models import Contact, Partner, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Partner
        fields = ['name', 'contact', 'supplier',
                  'products', 'debt', 'create_at']
        extra_kwargs = {'debt': {'read_only': True}}
        # datetime_format = '%Y-%m-%d %H:%M:%S'
        # date_format = '%Y-%m-%d %H:%M:%S'
