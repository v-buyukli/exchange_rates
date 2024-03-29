from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Rate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("vendor", models.CharField(max_length=255)),
                ("currency_a", models.CharField(max_length=3)),
                ("currency_b", models.CharField(max_length=3)),
                ("sell", models.DecimalField(decimal_places=2, max_digits=10)),
                ("buy", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
