# Generated by Django 4.1.5 on 2023-01-12 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_bookcopy_publisher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookcopy',
            options={'verbose_name_plural': 'Book copies'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
