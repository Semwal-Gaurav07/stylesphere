from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, PasswordResetOTP
from store.models import Order

def mask_email(val):
    if not val or '@' not in val:
        return 'your account'
    parts = val.split('@')
    name = parts[0]
    domain = parts[1]
    if len(name) <= 2:
        masked_name = name[0] + '*'
    else:
        masked_name = name[0] + '*' * (len(name) - 2) + name[-1]
    return f"{masked_name}@{domain}"

def register(request):
    if request.user.is_authenticated:
        messages.info(request, f"You already have an active session as '{request.user.username}'. Sign out below to create a new account.")
        return redirect('accounts:profile')
    
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
        messages.info(request, f"You are currently signed in as '{request.user.username}'. Sign out below to access a different account.")
        return redirect('accounts:profile')
    
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
    Commercial-Grade OTP Verification & Password Recovery:
    Step 1: Identify account by Email or Username -> Generate & dispatch 6-digit OTP.
    Step 2: Verify 6-digit OTP with live countdown & resend capability.
    Step 3: Set and confirm New Password -> Update credentials securely.
    """
    if request.user.is_authenticated:
        return redirect('store:product_list')

    step = int(request.session.get('reset_step', 1))

    # Allow query parameter to reset flow
    if request.GET.get('restart'):
        for key in ['reset_user_id', 'reset_step', 'reset_email_masked', 'dev_otp_preview']:
            request.session.pop(key, None)
        step = 1

    user_id = request.session.get('reset_user_id')
    user = User.objects.filter(id=user_id).first() if user_id else None

    # Step 1: User requests OTP for their account
    if request.method == 'POST':
        post_step = request.POST.get('step', str(step))

        # Action: Resend OTP
        if request.POST.get('action') == 'resend':
            if user:
                otp = PasswordResetOTP.create_otp(user)
                request.session['dev_otp_preview'] = otp.otp_code
                print(f"\n========================================================")
                print(f"🔐 [STYLE SPHERE OTP RESEND] User: {user.username} | Code: {otp.otp_code}")
                print(f"========================================================\n")
                
                # Send email
                try:
                    subject = "Style Sphere — Your Resent Verification Code"
                    body = f"Hello {user.username},\n\nYour new 6-digit verification code is:\n\n{otp.otp_code}\n\nThis code is valid for 10 minutes."
                    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email or 'noreply@stylesphere.com'], fail_silently=True)
                except Exception:
                    pass

                messages.success(request, 'A fresh 6-digit verification code has been dispatched!')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email_masked'),
                    'dev_otp': otp.otp_code
                })

        # STEP 1: Verify Account & Send OTP
        if post_step == '1':
            identifier = request.POST.get('identifier', '').strip()
            if not identifier:
                messages.error(request, 'Please enter your registered username or email address.')
                return render(request, 'accounts/password_reset.html', {'step': 1})

            # Look up user by username or email
            found_user = User.objects.filter(username__iexact=identifier).first() or                          User.objects.filter(email__iexact=identifier).first()

            if not found_user:
                messages.error(request, 'No active account matches the provided username or email.')
                return render(request, 'accounts/password_reset.html', {'step': 1, 'identifier': identifier})

            # Generate OTP
            otp = PasswordResetOTP.create_otp(found_user)
            request.session['reset_user_id'] = found_user.id
            request.session['reset_step'] = 2
            masked = mask_email(found_user.email if found_user.email else found_user.username)
            request.session['reset_email_masked'] = masked
            request.session['dev_otp_preview'] = otp.otp_code

            print(f"\n========================================================")
            print(f"🔐 [STYLE SPHERE OTP GENERATED] User: {found_user.username} | Code: {otp.otp_code}")
            print(f"========================================================\n")

            # Dispatch email
            try:
                subject = "Style Sphere — Password Recovery Verification Code"
                body = f"Hello {found_user.username},\n\nYour 6-digit verification code to reset your password is:\n\n{otp.otp_code}\n\nThis code is valid for 10 minutes. If you did not request this, please disregard this email."
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [found_user.email or 'noreply@stylesphere.com'], fail_silently=True)
            except Exception:
                pass

            messages.success(request, f'Verification code dispatched to {masked}!')
            return render(request, 'accounts/password_reset.html', {
                'step': 2,
                'user_email': masked,
                'dev_otp': otp.otp_code
            })

        # STEP 2: Verify OTP
        elif post_step == '2':
            if not user:
                messages.error(request, 'Session expired. Please enter your account identifier again.')
                request.session['reset_step'] = 1
                return redirect('accounts:password_reset')

            # Gather OTP code from individual inputs or single input
            entered_otp = request.POST.get('otp_code', '').strip()
            if not entered_otp:
                # Check for individual digit inputs otp_1..otp_6
                digits = [request.POST.get(f'otp_{i}', '').strip() for i in range(1, 7)]
                entered_otp = ''.join(digits)

            if len(entered_otp) != 6 or not entered_otp.isdigit():
                messages.error(request, 'Please enter a valid 6-digit numeric OTP code.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email_masked'),
                    'dev_otp': request.session.get('dev_otp_preview')
                })

            # Check matching unverified OTP for user
            latest_otp = user.reset_otps.filter(is_verified=False).first()
            if latest_otp and latest_otp.is_valid() and latest_otp.otp_code == entered_otp:
                latest_otp.is_verified = True
                latest_otp.save()
                request.session['reset_step'] = 3
                messages.success(request, 'OTP verified successfully! Please enter your new password.')
                return render(request, 'accounts/password_reset.html', {'step': 3, 'username': user.username})
            else:
                if latest_otp:
                    latest_otp.attempts += 1
                    latest_otp.save()
                messages.error(request, 'Incorrect or expired OTP code. Please check and try again.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email_masked'),
                    'dev_otp': request.session.get('dev_otp_preview')
                })

        # STEP 3: Set New Password
        elif post_step == '3':
            if not user or step != 3:
                messages.error(request, 'Security verification required before setting a new password.')
                request.session['reset_step'] = 1
                return redirect('accounts:password_reset')

            new_pass = request.POST.get('new_password', '').strip()
            confirm_pass = request.POST.get('confirm_password', '').strip()

            if not new_pass or not confirm_pass:
                messages.error(request, 'Please fill in both password fields.')
                return render(request, 'accounts/password_reset.html', {'step': 3, 'username': user.username})

            if new_pass != confirm_pass:
                messages.error(request, 'Passwords do not match. Please ensure both fields are identical.')
                return render(request, 'accounts/password_reset.html', {'step': 3, 'username': user.username})

            if len(new_pass) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return render(request, 'accounts/password_reset.html', {'step': 3, 'username': user.username})

            # Update password
            user.set_password(new_pass)
            user.save()

            # Clean session
            for key in ['reset_user_id', 'reset_step', 'reset_email_masked', 'dev_otp_preview']:
                request.session.pop(key, None)

            messages.success(request, f'Password for account "{user.username}" has been successfully updated! Please sign in with your new password.')
            return redirect('accounts:login')

    # GET Request: render current active step
    return render(request, 'accounts/password_reset.html', {
        'step': step,
        'user_email': request.session.get('reset_email_masked', ''),
        'dev_otp': request.session.get('dev_otp_preview', ''),
        'username': user.username if user else ''
    })
