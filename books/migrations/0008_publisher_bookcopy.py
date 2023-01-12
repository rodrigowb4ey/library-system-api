# Generated by Django 4.1.5 on 2023-01-12 18:16

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_category_book_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('date_published', models.DateField()),
                (
                    'book',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='books.book',
                    ),
                ),
                (
                    'publisher',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='books.publisher',
                    ),
                ),
            ],
        ),
    ]
