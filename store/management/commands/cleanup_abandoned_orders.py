from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.db.models import F, Q
from store.models import Order, Product

class Command(BaseCommand):
    help = 'Releases stock and marks abandoned unpaid orders older than 60 minutes as Cancelled'

    def add_arguments(self, parser):
        parser.add_argument(
            '--minutes',
            type=int,
            default=60,
            help='Age threshold in minutes for considering an order abandoned'
        )

    def handle(self, *args, **options):
        minutes = options['minutes']
        cutoff = timezone.now() - timedelta(minutes=minutes)
        abandoned_orders = Order.objects.filter(
            paid=False,
            status='Placed',
            created__lt=cutoff
        ).filter(
            Q(payment_method__icontains='Google Pay') | Q(payment_method__icontains='Pending')
        )

        count = 0
        for order in abandoned_orders:
            with transaction.atomic():
                for item in order.items.all():
                    item.product.variants.filter(size=item.size).update(stock=F('stock') + item.quantity)
                    Product.objects.filter(id=item.product.id).update(stock=F('stock') + item.quantity)
                    Product.objects.filter(id=item.product.id, available=False).update(available=True)

                order.status = 'Cancelled'
                order.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {count} abandoned orders and restored stock.'))
