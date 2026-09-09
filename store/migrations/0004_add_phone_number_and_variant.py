from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_add_tracking_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('S', 'Small (S)'), ('M', 'Medium (M)'), ('L', 'Large (L)'), ('XL', 'Extra Large (XL)'), ('XXL', 'Double Extra Large (XXL)')], max_length=10)),
                ('stock', models.PositiveIntegerField(default=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='store.product')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('product', 'size')},
            },
        ),
    ]
