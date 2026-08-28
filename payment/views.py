import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from store.models import Order
from store.notifications import generate_customer_whatsapp_url, generate_admin_order_alert_message

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
            order.payment_method = f'Credit/Debit Card (Ending in {last4})'
            order.payment_id = f"CARD-{order.id}-{last4}"
        elif payment_type == 'upi':
            upi_id = request.POST.get('upi_id', 'UPI Payment')
            order.paid = True
            order.payment_method = f'UPI ({upi_id})'
            order.payment_id = f"UPI-{order.id}"
        elif payment_type == 'razorpay':
            order.paid = True
            order.payment_method = 'Razorpay / UPI'
            order.payment_id = request.POST.get('razorpay_payment_id', f'RZP-{order.id}')
        else:
            order.paid = True
            order.payment_method = 'Online Payment'
            
        order.save()
        return redirect('payment:done')

    return render(request, 'payment/process.html', {
        'order': order,
        'razorpay_key_id': getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_stylesphere_live'),
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', 'pk_test_sample'),
        'store_upi_id': getattr(settings, 'STORE_UPI_ID', '9781855165@upi'),
    })

def payment_done(request):
    order_id = request.session.get('order_id')
    order = None
    whatsapp_url = None
    admin_alert_url = None
    if order_id:
        order = Order.objects.filter(id=order_id).first()
        if order:
            whatsapp_url = generate_customer_whatsapp_url(order)
            admin_alert_url = generate_admin_order_alert_message(order)
    return render(request, 'payment/done.html', {
        'order': order,
        'whatsapp_url': whatsapp_url,
        'admin_alert_url': admin_alert_url,
    })

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

@csrf_exempt
@require_POST
def razorpay_webhook(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        event = data.get('event')
        if event == 'payment.captured':
            payment_entity = data.get('payload', {}).get('payment', {}).get('entity', {})
            order_notes = payment_entity.get('notes', {})
            order_id = order_notes.get('order_id')
            if order_id:
                order = Order.objects.filter(id=order_id).first()
                if order:
                    order.paid = True
                    order.payment_id = payment_entity.get('id', '')
                    order.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = json.loads(payload.decode('utf-8'))
        if event.get('type') == 'checkout.session.completed':
            session = event.get('data', {}).get('object', {})
            order_id = session.get('client_reference_id')
            if order_id:
                order = Order.objects.filter(id=order_id).first()
                if order:
                    order.paid = True
                    order.payment_id = session.get('payment_intent', '')
                    order.save()
        return HttpResponse(status=200)
    except Exception:
        return HttpResponse(status=400)
