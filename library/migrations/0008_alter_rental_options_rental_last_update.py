# Generated by Django 5.0.6 on 2024-09-03 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_remove_rental_is_active_rental_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rental',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='rental',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
