# Generated by Django 5.0.6 on 2024-07-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='serial_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]
