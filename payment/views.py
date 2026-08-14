from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from store.models import Order

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Simulate successful payment confirmation
        order.paid = True
        order.save()
        return redirect('payment:done')

    return render(request, 'payment/process.html', {
        'order': order,
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
        'razorpay_key_id': getattr(settings, 'RAZORPAY_KEY_ID', '')
    })

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
