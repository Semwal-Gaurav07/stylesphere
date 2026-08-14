from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from store.models import Order

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        if payment_type == 'cod':
            order.paid = False
            order.payment_method = 'Cash on Delivery (COD)'
            order.save()
        else:
            order.paid = True
            order.payment_method = 'Online Payment'
            order.save()
        return redirect('payment:done')

    return render(request, 'payment/process.html', {
        'order': order,
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
        'razorpay_key_id': getattr(settings, 'RAZORPAY_KEY_ID', '')
    })

def payment_done(request):
    order_id = request.session.get('order_id')
    order = None
    if order_id:
        order = Order.objects.filter(id=order_id).first()
    return render(request, 'payment/done.html', {'order': order})

def payment_canceled(request):
    return render(request, 'payment/canceled.html')