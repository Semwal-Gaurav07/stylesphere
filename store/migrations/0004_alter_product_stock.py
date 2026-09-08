from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_add_tracking_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=15),
        ),
    ]
