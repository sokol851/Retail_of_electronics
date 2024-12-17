from relations.models import Product, Contact, Partner
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'model']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'city']


class PartnerSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = ['name', 'contact', 'supplier', 'product', 'debt', 'create_at']
        extra_kwargs = {'debt': {'read_only': True}}
