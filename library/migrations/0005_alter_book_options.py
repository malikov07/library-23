# Generated by Django 5.0.6 on 2024-07-27 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['last_update', 'created_date']},
        ),
    ]
