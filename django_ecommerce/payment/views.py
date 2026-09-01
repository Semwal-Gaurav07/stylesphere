from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from store.models import Order

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
        elif payment_type == 'upi':
            upi_id = request.POST.get('upi_id', 'UPI Payment')
            order.paid = True
            order.payment_method = f'UPI ({upi_id})'
        else:
            order.paid = True
            order.payment_method = 'Online Payment'
            
        order.save()
        return redirect('payment:done')

    return render(request, 'payment/process.html', {'order': order})

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
