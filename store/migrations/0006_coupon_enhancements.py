from django.db import migrations, models
from decimal import Decimal

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_phone_number_productvariant'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='max_uses',
            field=models.PositiveIntegerField(default=500),
        ),
        migrations.AddField(
            model_name='coupon',
            name='min_purchase',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='coupon',
            name='used_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
