# Generated by Django 4.2.6 on 2023-10-30 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_management", "0005_rename_is_discarded_taskcards_is_archived"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskcards",
            name="is_archived",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]