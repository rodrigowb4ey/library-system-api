# Generated by Django 4.1.5 on 2023-01-12 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_alter_bookcopy_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcopy',
            name='publisher',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='books.publisher',
            ),
        ),
    ]
