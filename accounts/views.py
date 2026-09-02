from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from store.models import Order

def register(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
    
    next_url = request.GET.get('next') or request.POST.get('next') or 'store:product_list'

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user)
            messages.success(request, f'Welcome, {new_user.username}! Your VIP account is active.')
            return redirect(next_url)
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'next': next_url})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
    
    next_url = request.GET.get('next') or request.POST.get('next') or 'store:product_list'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect(next_url)
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:product_list')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Shipping details updated successfully!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'orders': orders
    })

def password_reset_view(request):
    """
    Dual-mode password reset:
    1. Direct instant reset: Verify username + registered email and update password immediately.
    2. Email-based link: Send traditional reset token to user's email.
    """
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        reset_type = request.POST.get('reset_type', 'direct')

        if reset_type == 'direct':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()

            if not username or not email or not new_password:
                messages.error(request, 'Please complete all required fields.')
                return render(request, 'accounts/password_reset.html', {'active_tab': 'direct'})

            if new_password != confirm_password:
                messages.error(request, 'The two passwords do not match. Please try again.')
                return render(request, 'accounts/password_reset.html', {'active_tab': 'direct', 'username': username, 'email': email})

            if len(new_password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return render(request, 'accounts/password_reset.html', {'active_tab': 'direct', 'username': username, 'email': email})

            # Check if user exists with this username and email
            user_match = User.objects.filter(username__iexact=username, email__iexact=email).first()
            if not user_match:
                # Also try matching by username alone if email is blank on user record
                user_by_username = User.objects.filter(username__iexact=username).first()
                if user_by_username and not user_by_username.email:
                    user_match = user_by_username

            if user_match:
                user_match.set_password(new_password)
                if email and not user_match.email:
                    user_match.email = email
                user_match.save()
                messages.success(request, f'Password for "{user_match.username}" has been successfully updated! You can now sign in with your new password.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'No registered user matches the provided username and email address.')
                return render(request, 'accounts/password_reset.html', {'active_tab': 'direct', 'username': username, 'email': email})

        elif reset_type == 'email':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='accounts/password_reset_email.html',
                    subject_template_name='accounts/password_reset_subject.txt',
                )
                messages.success(request, 'If an account exists with that email address, a password reset link has been dispatched.')
                return redirect('accounts:password_reset_done')
            else:
                messages.error(request, 'Please provide a valid email address.')
                return render(request, 'accounts/password_reset.html', {'active_tab': 'email'})

    return render(request, 'accounts/password_reset.html', {'active_tab': 'direct'})
