from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rate",
            name="buy",
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
        migrations.AlterField(
            model_name="rate",
            name="sell",
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
    ]
