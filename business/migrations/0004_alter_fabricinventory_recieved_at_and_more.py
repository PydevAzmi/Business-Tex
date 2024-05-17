# Generated by Django 4.2 on 2024-05-16 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("business", "0003_alter_fabricdyeingfactory_came_out_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fabricinventory",
            name="recieved_at",
            field=models.DateField(default="2024-04-29", verbose_name="received at"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="fabricinventory",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.person",
                verbose_name="Supplier",
            ),
        ),
    ]