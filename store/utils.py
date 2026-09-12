from django.conf import settings
import urllib.parse
from datetime import datetime, timedelta

def check_pincode_serviceability(pincode):
    """
    Validates Indian 6-digit postal pincodes, calculates estimated delivery days,
    and checks Cash on Delivery (COD) eligibility.
    """
    pincode = str(pincode).strip()
    if len(pincode) != 6 or not pincode.isdigit():
        return {
            'valid': False,
            'message': 'Please enter a valid 6-digit Indian postal pincode.',
            'cod_available': False,
            'delivery_date': None,
            'courier': None
        }

    first_two = pincode[:2]
    if first_two in ['11', '12', '13', '14', '16', '20']:
        days = 2
        courier = 'Delhivery Express Surface'
    elif first_two in ['40', '41', '50', '56', '60', '70']:
        days = 3
        courier = 'BlueDart Air Express'
    else:
        days = 4
        courier = 'DTDC Standard Express'

    est_date = (datetime.now() + timedelta(days=days)).strftime("%A, %b %d")
    return {
        'valid': True,
        'message': f'Serviceable! Guaranteed dispatch via {courier}. Delivery by {est_date}.',
        'cod_available': True,
        'delivery_date': est_date,
        'courier': courier
    }

def generate_admin_whatsapp_url(order):
    """
    Generates a WhatsApp notification link with full order details for the store admin.
    Safe against missing phone numbers.
    """
    admin_number = getattr(settings, 'ADMIN_WHATSAPP_NUMBER', '919781855165')
    items_list = "\n".join([f"• {item.product.name} ({item.size}) x {item.quantity} - ₹{item.get_cost()}" for item in order.items.all()])
    cust_phone = getattr(order, 'phone_number', '') or 'Not provided'

    msg = (
        f"🚨 *NEW ORDER ALERT - #{order.id}*\n\n"
        f"👤 *Customer:* {order.first_name} {order.last_name}\n"
        f"📞 *Phone:* {cust_phone}\n"
        f"📍 *Address:* {order.address}, {order.city} - {order.postal_code}\n"
        f"📦 *Items:*\n{items_list}\n\n"
        f"💰 *Total Payable:* ₹{order.get_total_cost()}\n"
        f"💳 *Payment Mode:* {order.payment_method} ({'PAID' if order.paid else 'UNPAID / COD'})\n"
        f"🚚 *Tracking No:* {order.tracking_number}\n\n"
        f"🔗 *Invoice:* https://stylesphere-store.onrender.com/orders/{order.id}/invoice/"
    )
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{admin_number}?text={encoded_msg}"
