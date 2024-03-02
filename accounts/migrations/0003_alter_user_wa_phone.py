# Generated by Django 4.2 on 2024-03-02 16:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_location_address_alter_location_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="wa_phone",
            field=models.CharField(
                max_length=14, unique=True, verbose_name="Whatsapp Phone Number"
            ),
        ),
    ]
