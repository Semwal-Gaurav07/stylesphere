import urllib.parse
from django.conf import settings

def generate_customer_whatsapp_url(order):
    phone = getattr(settings, 'STORE_WHATSAPP_NUMBER', '919781855165')
    items_list = "%0A".join([f"• {item.quantity}x {item.product.name} (Size: {item.size})" for item in order.items.all()])
    message = (
        f"🔥 *Style Sphere Order Confirmation*%0A"
        f"Hi {order.first_name}, your order *#{order.id}* is confirmed!%0A%0A"
        f"*Items Ordered:*%0A{items_list}%0A%0A"
        f"💰 *Total Due:* ₹{order.get_total_cost()}%0A"
        f"💳 *Payment Mode:* {order.payment_method}%0A"
        f"🚚 *Tracking AWB:* {order.tracking_number or f'SS-IND-{order.id:06d}'}%0A"
        f"📍 *Shipping To:* {order.address}, {order.city} ({order.postal_code})%0A%0A"
        f"Need help with your order? Reply directly to this chat."
    )
    return f"https://wa.me/{phone}?text={message}"

def generate_admin_order_alert_message(order):
    items_summary = ", ".join([f"{item.quantity}x {item.product.name} ({item.size})" for item in order.items.all()])
    text = (
        f"🚨 *NEW ORDER ALERT - #{order.id}*%0A"
        f"👤 Customer: {order.first_name} {order.last_name}%0A"
        f"📞 Phone/Email: {order.phone or order.email}%0A"
        f"📦 Items: {items_summary}%0A"
        f"💰 Total: ₹{order.get_total_cost()} ({order.payment_method})%0A"
        f"📍 City: {order.city} - {order.postal_code}"
    )
    phone = getattr(settings, 'STORE_WHATSAPP_NUMBER', '919781855165')
    return f"https://wa.me/{phone}?text={text}"
