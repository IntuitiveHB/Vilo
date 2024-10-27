# Generated by Django 4.2.5 on 2023-10-18 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_remove_customuser_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="client_type",
            field=models.CharField(
                choices=[("individual", "INDIVIDUAL"), ("company", "COMPANY")],
                max_length=50,
                null=True,
                verbose_name="Client Type",
            ),
        ),
    ]