from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
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
            # Automatically log the user in
            login(request, new_user)
            messages.success(request, f'Welcome, {new_user.username}! Your account has been created.')
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
            messages.success(request, 'Your profile has been updated!')
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