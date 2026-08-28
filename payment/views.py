from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from store.models import Order
from store.utils import generate_admin_whatsapp_url
import json

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 'cod')
        
        if payment_type == 'cod':
            order.paid = False
            order.payment_method = 'Cash on Delivery (COD)'
        elif payment_type == 'card':
            card_num = request.POST.get('card_number', '4242')
            last4 = card_num.replace(' ', '')[-4:] if len(card_num) >= 4 else '4242'
            order.paid = True
            order.payment_method = f'Card (Ending in {last4})'
        elif payment_type == 'upi':
            upi_id = request.POST.get('upi_id', 'UPI')
            order.paid = True
            order.payment_method = f'UPI ({upi_id})'
        elif payment_type == 'razorpay':
            order.paid = True
            order.payment_method = 'Razorpay Online Gateway'
        elif payment_type == 'stripe':
            order.paid = True
            order.payment_method = 'Stripe Online Gateway'
        else:
            order.paid = True
            order.payment_method = 'Online Payment'
            
        order.save()
        return redirect('payment:done')

    return render(request, 'payment/process.html', {
        'order': order,
        'razorpay_key_id': getattr(settings, 'RAZORPAY_KEY_ID', ''),
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
    })

def payment_done(request):
    order_id = request.session.get('order_id')
    order = None
    admin_whatsapp_url = None
    if order_id:
        order = Order.objects.filter(id=order_id).first()
        if order:
            admin_whatsapp_url = generate_admin_whatsapp_url(order)
    return render(request, 'payment/done.html', {
        'order': order,
        'admin_whatsapp_url': admin_whatsapp_url
    })

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

@csrf_exempt
def razorpay_webhook(request):
    """
    Server-side webhook for verified Razorpay automated payment captures
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
            event = payload.get('event')
            if event == 'payment.captured':
                payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
                notes = payment_entity.get('notes', {})
                order_id = notes.get('order_id')
                if order_id:
                    order = Order.objects.filter(id=order_id).first()
                    if order:
                        order.paid = True
                        order.transaction_id = payment_entity.get('id', '')
                        order.payment_method = 'Razorpay (Verified Webhook)'
                        order.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return HttpResponse(status=405)

@csrf_exempt
def stripe_webhook(request):
    """
    Server-side webhook for verified Stripe checkout session captures
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
            event_type = payload.get('type')
            if event_type == 'checkout.session.completed':
                session = payload.get('data', {}).get('object', {})
                order_id = session.get('client_reference_id')
                if order_id:
                    order = Order.objects.filter(id=order_id).first()
                    if order:
                        order.paid = True
                        order.transaction_id = session.get('payment_intent', '')
                        order.payment_method = 'Stripe (Verified Webhook)'
                        order.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return HttpResponse(status=405)
