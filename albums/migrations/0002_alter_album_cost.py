# Generated by Django 4.2.5 on 2024-02-08 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=1000.0, max_digits=10),
        ),
    ]
