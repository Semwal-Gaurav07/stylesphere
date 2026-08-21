import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Order, OrderItem, Wishlist, Review, Product, Category, Coupon
from accounts.models import Profile

def inspect_all_users():
    users = User.objects.all()
    print("=" * 65)
    print(f"TOTAL REGISTERED USERS IN DATABASE: {users.count()}")
    print("=" * 65)

    if not users.exists():
        print("No users found in database.")
        return

    for u in users:
        print(f"\n?? USER: {u.username} (ID: {u.id})")
        print(f"   • Name: {u.get_full_name() or 'Not set'}")
        print(f"   • Email: {u.email or 'Not set'}")
        print(f"   • Is Superuser: {u.is_superuser}")
        print(f"   • Date Joined: {u.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")

        profile = Profile.objects.filter(user=u).first()
        if profile:
            print(f"   • Saved Shipping Address:")
            print(f"     - Phone: {profile.phone_number or 'Not set'}")
            print(f"     - Address: {profile.address or 'Not set'}")
            print(f"     - City: {profile.city or 'Not set'}")
            print(f"     - Pincode: {profile.postal_code or 'Not set'}")
        else:
            print(f"   • Saved Profile: None")

        wishlist_items = Wishlist.objects.filter(user=u)
        print(f"   • Wishlist ({wishlist_items.count()} items):")
        if wishlist_items.exists():
            for w in wishlist_items:
                print(f"     - {w.product.name} (?{w.product.price})")
        else:
            print("     - (No items saved)")

        orders = Order.objects.filter(user=u)
        print(f"   • Orders Placed ({orders.count()} orders):")
        if orders.exists():
            for o in orders:
                print(f"     ?? Order #{o.id} | Date: {o.created.strftime('%Y-%m-%d %H:%M')} | Status: {o.status}")
                print(f"        - Payment: {o.payment_method} | Paid: {'Yes' if o.paid else 'No (COD)'}")
                print(f"        - Shipping to: {o.first_name} {o.last_name}, {o.address}, {o.city} - {o.postal_code}")
                for item in o.items.all():
                    print(f"        - Item: {item.quantity}x {item.product.name} (Size: {item.size}, Price: ?{item.price})")
                print(f"        - Total Cost: ?{o.get_total_cost()}")
        else:
            print("     - (No orders placed)")

        reviews = Review.objects.filter(user=u)
        print(f"   • Customer Reviews ({reviews.count()} submitted):")
        if reviews.exists():
            for r in reviews:
                print(f"     ? {r.product.name}: {r.rating}/5 — \"{r.comment}\" ({r.created.strftime('%Y-%m-%d')})")
        else:
            print("     - (No reviews submitted)")

        print("-" * 65)

if __name__ == '__main__':
    inspect_all_users()
