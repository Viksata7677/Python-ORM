# Generated by Django 5.0.4 on 2024-06-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='name',
            field=models.CharField(default=1, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
