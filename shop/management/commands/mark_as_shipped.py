import random
from django.core.management.base import BaseCommand
from shop.models import Order

class Command(BaseCommand):
    help = 'Generate tracking IDs for processing orders and mark them as shipped'

    def handle(self, *args, **kwargs):
        processing_orders = Order.objects.filter(status='processing')
        for order in processing_orders:
            order.tracking_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            order.status = 'shipped'
            order.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated orders'))
