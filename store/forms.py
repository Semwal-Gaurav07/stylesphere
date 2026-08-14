from django import forms
from .models import Order, Review

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, initial=1)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

class CouponApplyForm(forms.Form):
    code = forms.CharField(label='Promo Code', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g. FIRST10'
    }))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select mb-3'}),
            'comment': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3, 'placeholder': 'Share your experience with this product...'}),
        }