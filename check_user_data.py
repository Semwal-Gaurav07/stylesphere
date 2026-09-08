import os
import django

# Initialize Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Order, Wishlist, Review
from accounts.models import Profile

def inspect_all_users():
    users = User.objects.all().order_by('-date_joined')
    count = users.count()

    print("=" * 65)
    print(f"  TOTAL REGISTERED CLIENTS / USERS: {count}")
    print("=" * 65)

    if not users.exists():
        print("\nNo registered users found in the database yet.")
        print("Users will appear here once they register via /accounts/register/")
        return

    for idx, u in enumerate(users, 1):
        print(f"\n[{idx}] USER: {u.username} (ID: {u.id})")
        print(f"    • Full Name:    {u.get_full_name() or 'Not specified'}")
        print(f"    • Email:        {u.email or 'Not specified'}")
        print(f"    • Is Staff:     {u.is_staff}")
        print(f"    • Date Joined:  {u.date_joined.strftime('%d %B %Y, %I:%M %p')}")

        # Profile Data
        profile = Profile.objects.filter(user=u).first()
        if profile:
            addr = profile.address or 'None'
            city = profile.city or 'None'
            pin = profile.postal_code or 'None'
            phone = profile.phone_number or 'None'
            print(f"    • Shipping Info: {addr}, {city} - {pin} (Phone: {phone})")

        # Stats
        orders_count = Order.objects.filter(user=u).count()
        wishlist_count = Wishlist.objects.filter(user=u).count()
        reviews_count = Review.objects.filter(user=u).count()
        print(f"    • Activity:     {orders_count} orders placed | {wishlist_count} wishlist items | {reviews_count} reviews")

    print("\n" + "=" * 65)

if __name__ == '__main__':
    inspect_all_users()
