# Generated by Django 4.2.13 on 2024-05-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nlp_classifier", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="prediction",
            name="generate_time",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="prediction",
            name="total_time",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]