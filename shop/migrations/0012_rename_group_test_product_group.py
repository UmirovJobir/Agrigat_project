# Generated by Django 4.1.5 on 2023-05-29 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_rename_group_id_product_group_old_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='group_test',
            new_name='group',
        ),
    ]