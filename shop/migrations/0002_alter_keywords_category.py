# Generated by Django 4.1.5 on 2023-03-25 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keywords',
            name='category',
            field=models.IntegerField(),
        ),
    ]
