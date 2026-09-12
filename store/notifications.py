import threading
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta

def _async_send(subject, message, from_email, recipient):
    """Executes SMTP socket connection on background worker thread."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient],
            fail_silently=True
        )
        print(f"📧 [BACKGROUND EMAIL SUCCESS] Delivered order update to: {recipient}")
    except Exception as e:
        print(f"📧 [BACKGROUND EMAIL ERROR] Failed to send to {recipient}: {e}")

def send_order_confirmation_email(order):
    """
    Sends an automated, branded luxury order confirmation email to the customer.
    Dispatched via a background thread to prevent UI freezing during checkout.
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
Payment Status: {'PAID (Verified)' if order.paid else 'PENDING COLLECTION / COD'}

PIECES ORDERED:
{items_text}
TOTAL PAYABLE: ₹{order.get_total_cost()} (Inclusive of all taxes & insured air shipping)

DISPATCH DESTINATION:
{order.first_name} {order.last_name}
{order.address}
{order.city}, PIN: {order.postal_code}

AIR LOGISTICS & COURIER TRACKING:
Air Waybill (AWB): {order.awb_code}
Logistics Partner: Bluedart Express / Delhivery Air
Estimated Delivery: {est_delivery}

Client Services & Concierge:
WhatsApp: +91 9781855165 | Email: concierge@stylesphere.in

STYLE SPHERE ATELIER INC.
Industrial Area Phase 2, Panchkula, Haryana 134113
------------------------------------------------------------
"""

    print("\n" + "="*60)
    print(f"📧 [NON-BLOCKING TRANSACTIONAL DISPATCH]")
    print(f"To: {recipient} | Order #{order.id} | Amount: ₹{order.get_total_cost()} | AWB: {order.awb_code}")
    print("="*60 + "\n")

    # Fire and forget on daemon thread
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Style Sphere Atelier <noreply@stylesphere.in>')
    email_thread = threading.Thread(
        target=_async_send,
        args=(subject, message, from_email, recipient),
        daemon=True
    )
    email_thread.start()
    return True
