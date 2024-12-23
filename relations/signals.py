from django.db.models.signals import post_delete
from django.dispatch import receiver

from relations.models import Partner, Product


@receiver(post_delete, sender=Partner)
def related_contact_delete(sender, instance, **kwargs):
    """ Сигнал для удаления связанных объектов """
    products = list(Product.objects.all())

    for product in products:
        # Проверяем связь с другими партнёрами
        if not product.partner_set.exists():
            product.delete()  # Удаляем продукт, если нет связей

    # Удаляем контакт
    instance.contact.delete()
