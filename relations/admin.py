from django.contrib import admin, messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from relations.models import Contact, Partner, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "country",
        "city",
        "street",
        "house_number",
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type_organization",
        "city",
        "contact",
        "supplier_link",
        "debt",
    )
    list_filter = ('contact__city',)
    actions = ['clear_debt']

    @admin.action(description="Очистить задолженность")
    def clear_debt(self, request, queryset):
        """ Очищает задолженность """
        updated = queryset.update(debt=0)

        # Добавляем уведомление об успешной операции
        self.message_user(
            request,
            ngettext(
                "%d задолженность очищена.",
                "%d задолженности очищены.",
                updated,
            )
            % updated,
            messages.SUCCESS
        )

    def city(self, obj):
        """ Задаём кастомное поле города партнёра """
        return obj.contact.city

    # Переименовываем поле города и делаем его доступным для сортировки
    city.allow_tags = True
    city.admin_order_field = 'supplier'
    city.short_description = 'Город'

    def supplier_link(self, obj):
        """ Создаём ссылку, если есть поставщик """
        if obj.supplier:
            url = mark_safe('<a href="{0}">{1}</a>'.
                            format(reverse('admin:relations_partner_change',
                                           args=(obj.supplier.pk,)),
                                   obj.supplier))
            return url
        else:
            return "-"

    # Переименовываем поле поставщика и делаем его доступным для сортировки
    supplier_link.allow_tags = True  # Включаем
    supplier_link.admin_order_field = 'supplier'
    supplier_link.short_description = Partner.supplier.field.verbose_name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "model",
        "release_date",
    )
