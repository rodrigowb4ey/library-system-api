# Generated by Django 4.1.5 on 2023-01-12 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_bookcopy_options_alter_category_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='cover',
        ),
        migrations.AddField(
            model_name='bookcopy',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers'),
        ),
    ]
