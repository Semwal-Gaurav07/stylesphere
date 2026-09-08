from django.db import migrations, models
import django.db.models.deletion

def create_table_if_not_exists(apps, schema_editor):
    table_name = 'store_productvariant'
    try:
        tables = schema_editor.connection.introspection.table_names()
        if table_name not in tables:
            ProductVariant = apps.get_model('store', 'ProductVariant')
            schema_editor.create_model(ProductVariant)
    except Exception as e:
        print(f"Note: table creation handled ({e})")

def add_column_if_not_exists(apps, schema_editor):
    table_name = 'store_order'
    try:
        cursor = schema_editor.connection.cursor()
        columns = [col.name for col in schema_editor.connection.introspection.get_table_description(cursor, table_name)]
        if 'phone_number' not in columns:
            Order = apps.get_model('store', 'Order')
            field = models.CharField(blank=True, default='', max_length=20)
            field.set_attributes_from_name('phone_number')
            schema_editor.add_field(Order, field)
    except Exception as e:
        print(f"Note: column addition handled ({e})")

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_stock'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
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
            ],
            database_operations=[
                migrations.RunPython(add_column_if_not_exists, reverse_code=migrations.RunPython.noop),
                migrations.RunPython(create_table_if_not_exists, reverse_code=migrations.RunPython.noop),
            ]
        )
    ]
