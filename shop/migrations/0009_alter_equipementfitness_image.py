# Generated by Django 5.2 on 2025-05-08 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_equipementfitness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipementfitness',
            name='image',
            field=models.CharField(max_length=255),
        ),
    ]
