# Generated by Django 5.0.6 on 2024-07-25 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sinf',
            options={'ordering': ['number', 'letter']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['sinf', 'first_name', 'last_name']},
        ),
    ]
