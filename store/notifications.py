from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta

def send_order_confirmation_email(order):
    """
    Sends an automated, branded luxury order confirmation email to the customer.
    Gracefully handles console backend during local development and SMTP in production.
    """
    if not order or not order.email:
        return False

    recipient = order.email
    subject = f"Style Sphere Atelier — Order #{order.id} Confirmed (AWB: {order.awb_code})"

    # Calculate estimated delivery date
    est_delivery = (datetime.now() + timedelta(days=4)).strftime("%A, %B %d, %Y")

    items_text = ""
    for item in order.items.all():
        items_text += f"  • {item.product.name} | Size: {item.size} | Qty: {item.quantity} | ₹{item.get_cost()}\n"

    message = f"""STYLE SPHERE ATELIER DE COUTURE
ORDER CONFIRMATION & TRANSIT RECEIPT
------------------------------------------------------------
Dear {order.first_name} {order.last_name},

Thank you for your patronage. Your order has been confirmed and
is currently being prepped for dispatch in tamper-evident packaging.

ORDER DETAILS:
Order Number: #{order.id}
Date: {order.created.strftime('%d %B %Y, %I:%M %p')}
Payment Method: {order.payment_method}
Payment Status: {'PAID (Verified)' if order.paid else 'CASH ON DELIVERY (Pending Collection)'}

PIECES ORDERED:
{items_text}
TOTAL COST: ₹{order.get_total_cost()} (Inclusive of all taxes & complimentary insured shipping)

DISPATCH DESTINATION:
{order.first_name} {order.last_name}
{order.address}
{order.city}, PIN: {order.postal_code}

AIR LOGISTICS & COURIER TRACKING:
Air Waybill (AWB): {order.awb_code}
Logistics Partner: Bluedart Express / Delhivery Air
Estimated Delivery: {est_delivery}

You can track your order status in real time through your Atelier client dashboard
or view your official Tax Invoice online.

Client Services & Concierge:
WhatsApp: +91 9781855165 | Email: concierge@stylesphere.in

STYLE SPHERE ATELIER INC.
Industrial Area Phase 2, Panchkula, Haryana 134113
------------------------------------------------------------
"""

    print("\n" + "="*60)
    print(f"📧 [STYLE SPHERE TRANSACTIONAL EMAIL DISPATCHED]")
    print(f"To: {recipient} | Subject: {subject}")
    print(f"Order #{order.id} | Amount: ₹{order.get_total_cost()} | AWB: {order.awb_code}")
    print("="*60 + "\n")

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'Style Sphere Atelier <noreply@stylesphere.in>'),
            recipient_list=[recipient],
            fail_silently=True
        )
        return True
    except Exception as e:
        print(f"Email dispatch note: {e}")
        return False
