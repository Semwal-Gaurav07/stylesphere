from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from store.models import Order
from store.notifications import send_order_confirmation_email

try:
    import razorpay
except ImportError:
    razorpay = None

def get_razorpay_client():
    if razorpay and hasattr(settings, 'RAZORPAY_KEY_ID') and hasattr(settings, 'RAZORPAY_KEY_SECRET'):
        return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    return None

def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('store:product_list')

    order = get_object_or_404(Order, id=order_id)
    amount_in_paise = int(order.get_total_cost() * 100)
    razorpay_key = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_stylesphere2026')
    razorpay_order_id = f"order_{order.id}_demo"

    # Try creating real Razorpay order if credentials provided
    client = get_razorpay_client()
    if client:
        try:
            rzp_order = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'receipt': f'receipt_order_{order.id}',
                'payment_capture': 1
            })
            razorpay_order_id = rzp_order['id']
        except Exception as e:
            print(f"Razorpay Client Order Creation Note: {e}")
            razorpay_order_id = f"rzp_order_{order.id}"

    # Handle standard POST fallback (COD or Razorpay checkout redirection)
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 'cod')
        
        if payment_type == 'cod':
            order.paid = False
            order.payment_method = 'Cash on Delivery (COD)'
            order.save()
            send_order_confirmation_email(order)
            return redirect('payment:done')
        else:
            # Card / UPI / NetBanking must be processed via verified Razorpay checkout
            messages.info(request, 'Please complete payment using the secure Razorpay portal below.')
            return redirect('payment:process')

    return render(request, 'payment/process.html', {
        'order': order,
        'razorpay_key': razorpay_key,
        'razorpay_order_id': razorpay_order_id,
        'amount_in_paise': amount_in_paise
    })

@csrf_exempt
def payment_verify(request):
    """
    Handles Razorpay checkout callback verification.
    """
    if request.method == 'POST':
        order_id = request.session.get('order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        rzp_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        order = None
        if order_id:
            order = Order.objects.filter(id=order_id).first()

        if not order and rzp_order_id:
            # Fallback: extract order id from custom tracking
            try:
                raw_id = int(request.GET.get('order_id', 0))
                if raw_id:
                    order = Order.objects.filter(id=raw_id).first()
            except Exception:
                pass

        if order:
            client = get_razorpay_client()
            verified = False
            if client and signature and payment_id and rzp_order_id:
                try:
                    client.utility.verify_payment_signature({
                        'razorpay_order_id': rzp_order_id,
                        'razorpay_payment_id': payment_id,
                        'razorpay_signature': signature
                    })
                    verified = True
                except Exception as e:
                    print(f"Razorpay Signature Warning: {e}")
                    verified = False

            if verified:
                order.paid = True
                order.payment_method = f"Razorpay Online ({payment_id if payment_id else 'Verified'})"
                order.save()
                send_order_confirmation_email(order)
                messages.success(request, 'Online payment verified successfully! Your order has been placed.')
                return redirect('payment:done')
            else:
                messages.error(request, 'Payment signature verification failed. Please try again or use Cash on Delivery.')
                return redirect('payment:process')

    return redirect('payment:process')

def payment_done(request):
    order_id = request.session.get('order_id')
    order = None
    if order_id:
        order = Order.objects.filter(id=order_id).first()
    return render(request, 'payment/done.html', {'order': order})

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

@csrf_exempt
def webhook_handler(request):
    """
    Server-side Webhook endpoint for live payment gateways (Razorpay).
    Verifies cryptographic webhook signature and updates order status.
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
    signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')

    if webhook_secret and signature:
        import hmac
        import hashlib
        expected_sig = hmac.new(
            webhook_secret.encode('utf-8'),
            request.body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, signature):
            return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)

    try:
        import json
        payload = json.loads(request.body.decode('utf-8'))
        event = payload.get('event')

        if event in ['payment.captured', 'order.paid']:
            payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
            rzp_order_id = payment_entity.get('order_id')
            payment_id = payment_entity.get('id')

            order = None
            if rzp_order_id:
                order = Order.objects.filter(awb_code__icontains=rzp_order_id).first()
            if not order and 'notes' in payment_entity:
                order_id = payment_entity['notes'].get('order_id')
                if order_id:
                    order = Order.objects.filter(id=order_id).first()

            if order and not order.paid:
                order.paid = True
                order.payment_method = f"Razorpay Webhook ({payment_id or 'Verified'})"
                order.save()
                send_order_confirmation_email(order)

        return JsonResponse({'status': 'success', 'message': 'Webhook processed'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
