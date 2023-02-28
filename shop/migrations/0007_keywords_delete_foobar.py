# Generated by Django 4.1.5 on 2023-02-28 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_words', models.CharField(max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='shop.category')),
            ],
        ),
        migrations.DeleteModel(
            name='Foobar',
        ),
    ]
