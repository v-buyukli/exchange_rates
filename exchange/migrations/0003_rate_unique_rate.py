from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0002_alter_rate_buy_alter_rate_sell"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="rate",
            constraint=models.UniqueConstraint(
                fields=("date", "vendor", "currency_a", "currency_b"),
                name="unique_rate",
            ),
        ),
    ]
