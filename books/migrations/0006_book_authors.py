# Generated by Django 4.1.5 on 2023-01-12 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_alter_author_id'),
        ('books', '0005_alter_book_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='authors.author'),
        ),
    ]