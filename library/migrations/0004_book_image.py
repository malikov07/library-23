# Generated by Django 5.0.6 on 2024-07-25 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_rental_options_rental_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=1, upload_to='library/books'),
            preserve_default=False,
        ),
    ]
