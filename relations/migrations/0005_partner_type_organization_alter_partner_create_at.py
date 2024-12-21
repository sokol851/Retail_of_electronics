# Generated by Django 5.1.4 on 2024-12-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0004_alter_partner_create_at_alter_partner_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='type_organization',
            field=models.IntegerField(choices=[(0, 'Завод'), (1, 'Розничная сеть'), (2, 'ИП')], default=2, verbose_name='Тип организации'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partner',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
    ]