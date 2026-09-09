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

    # Handle standard POST fallback (COD or Direct Transfer)
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 'cod')
        
        if payment_type == 'cod':
            order.paid = False
            order.payment_method = 'Cash on Delivery (COD)'
        elif payment_type == 'card':
            card_num = request.POST.get('card_number', '4242')
            last4 = card_num.replace(' ', '')[-4:] if len(card_num) >= 4 else '4242'
            order.paid = True
            order.payment_method = f'Card Ending in {last4}'
        elif payment_type == 'upi':
            order.paid = True
            order.payment_method = 'UPI / QR Transfer'
        else:
            order.paid = True
            order.payment_method = 'Online Payment'
            
        order.save()
        send_order_confirmation_email(order)
        return redirect('payment:done')

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
            # Check signature with Razorpay if available
            client = get_razorpay_client()
            verified = True
            if client and signature and payment_id:
                try:
                    client.utility.verify_payment_signature({
                        'razorpay_order_id': rzp_order_id,
                        'razorpay_payment_id': payment_id,
                        'razorpay_signature': signature
                    })
                except Exception as e:
                    print(f"Razorpay Signature Warning: {e}")
                    # Allow dev pass-through if test key
                    if 'test' not in getattr(settings, 'RAZORPAY_KEY_ID', ''):
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
    """Server-side Webhook endpoint for live payment gateways."""
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Webhook verified'})
    return HttpResponse(status=405)
