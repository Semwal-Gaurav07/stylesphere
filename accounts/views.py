from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, f"You are currently signed in as '{request.user.username}'.")
        return redirect('accounts:profile')
    
    next_url = request.GET.get('next') or request.POST.get('next') or 'store:product_list'

    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not identifier or not password:
            messages.error(request, 'Please enter both your username/email and password.')
            return render(request, 'accounts/login.html', {'next': next_url})

        # 1. Authenticate directly by username
        user = authenticate(username=identifier, password=password)

        # 2. If not matched, try authenticating by email
        if user is None:
            matched_user = User.objects.filter(email__iexact=identifier).first()
            if matched_user:
                user = authenticate(username=matched_user.username, password=password)

        # 3. Case-insensitive username fallback
        if user is None:
            matched_user = User.objects.filter(username__iexact=identifier).first()
            if matched_user:
                user = authenticate(username=matched_user.username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'This account is currently disabled.')
        else:
            messages.error(request, 'Invalid username or password. Please verify your credentials or reset your password.')
    
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:product_list')

@csrf_exempt
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

@csrf_exempt
def password_reset_view(request):
    """
    Commercial-Grade OTP Verification & Password Recovery:
    Step 1: Identify account by Email or Username -> Generate & dispatch 6-digit OTP.
    Step 2: Verify 6-digit OTP with auto-advance, paste support, and live countdown.
    Step 3: Set and confirm New Password -> Update credentials securely.
    """
    if request.user.is_authenticated:
        return redirect('store:product_list')

    # Allow query parameter to reset flow
    if request.GET.get('restart'):
        for key in ['reset_user_id', 'reset_step', 'reset_email_masked', 'dev_otp_preview']:
            request.session.pop(key, None)
        request.session.modified = True
        return redirect('accounts:password_reset')

    step = int(request.session.get('reset_step', 1))
    user_id = request.session.get('reset_user_id')
    user = User.objects.filter(id=user_id).first() if user_id else None

    # Auto-heal: If user state is lost on step 2 or 3, return to step 1
    if not user and step > 1:
        step = 1
        request.session['reset_step'] = 1
        request.session.modified = True

    if request.method == 'POST':
        post_step = request.POST.get('step', str(step))

        # ================= STEP 1: VERIFY ACCOUNT & DISPATCH OTP =================
        if post_step == '1':
            identifier = request.POST.get('identifier', '').strip()
            if not identifier:
                messages.error(request, 'Please enter your registered username or email address.')
                return render(request, 'accounts/password_reset.html', {'step': 1})

            # Look up user by username or email
            found_user = User.objects.filter(username__iexact=identifier).first() or \
                         User.objects.filter(email__iexact=identifier).first()

            if not found_user:
                messages.error(request, 'No active account matches the provided username or email.')
                return render(request, 'accounts/password_reset.html', {'step': 1, 'identifier': identifier})

            if not found_user.email:
                messages.error(request, f'The account "{found_user.username}" has no registered email address on file. Please contact Atelier concierge on WhatsApp (+91 9781855165) for manual verification.')
                return render(request, 'accounts/password_reset.html', {'step': 1, 'identifier': identifier})

            # Generate fresh cryptographically secure OTP
            otp = PasswordResetOTP.create_otp(found_user)
            request.session['reset_user_id'] = found_user.id
            request.session['reset_step'] = 2
            masked = mask_email(found_user.email)
            request.session['reset_email_masked'] = masked

            # Developer / Test mode helper badge
            is_dev = getattr(settings, 'DEBUG', True) or 'console' in getattr(settings, 'EMAIL_BACKEND', '').lower()
            dev_otp = otp.otp_code if is_dev else None
            request.session['dev_otp_preview'] = dev_otp or ''
            request.session.modified = True

            # Print to server logs
            print("\n" + "=" * 65)
            print(f"🔑 [STYLE SPHERE OTP DISPATCHED]")
            print(f"To: {found_user.email} (Username: {found_user.username})")
            print(f"Verification Code: {otp.otp_code} | Valid for: 10 minutes")
            print("=" * 65 + "\n")

            # Dispatch transactional email
            email_sent = False
            try:
                subject = "Style Sphere — Password Recovery Verification Code"
                body = (
                    f"Hello {found_user.username},\n\n"
                    f"Your 6-digit verification code to reset your Style Sphere account password is:\n\n"
                    f"  {otp.otp_code}\n\n"
                    f"This code is valid for 10 minutes.\n"
                    f"If you did not initiate this request, please ignore this email.\n\n"
                    f"— Style Sphere Atelier Support"
                )
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'Style Sphere <noreply@stylesphere.in>'),
                    recipient_list=[found_user.email],
                    fail_silently=False
                )
                email_sent = True
            except Exception as e:
                print(f"Email dispatch warning: {e}")

            if is_dev and not email_sent:
                messages.info(request, f"Verification code generated for {masked}. (Testing mode: see the verification code in the test badge below).")
            else:
                messages.success(request, f"Verification code dispatched to {masked}!")

            return render(request, 'accounts/password_reset.html', {
                'step': 2,
                'user_email': masked,
                'dev_otp': dev_otp
            })

        # ================= STEP 2: VERIFY 6-DIGIT OTP =================
        elif post_step == '2':
            if not user:
                messages.error(request, 'Session expired. Please enter your account identifier again.')
                request.session['reset_step'] = 1
                request.session.modified = True
                return redirect('accounts:password_reset')

            # Action: Resend OTP
            if request.POST.get('action') == 'resend':
                otp = PasswordResetOTP.create_otp(user)
                is_dev = getattr(settings, 'DEBUG', True) or 'console' in getattr(settings, 'EMAIL_BACKEND', '').lower()
                dev_otp = otp.otp_code if is_dev else None
                request.session['dev_otp_preview'] = dev_otp or ''
                request.session.modified = True

                print(f"\n🔑 [STYLE SPHERE RESENT OTP] User: {user.username} | Code: {otp.otp_code}\n")

                try:
                    subject = "Style Sphere — Your Resent Verification Code"
                    body = f"Hello {user.username},\n\nYour new 6-digit verification code is:\n\n  {otp.otp_code}\n\nValid for 10 minutes."
                    send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@stylesphere.in'), [user.email], fail_silently=True)
                except Exception:
                    pass

                messages.success(request, 'A fresh 6-digit verification code has been dispatched!')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email_masked'),
                    'dev_otp': dev_otp
                })

            # Assemble OTP from full hidden input or individual digit inputs
            entered_otp = request.POST.get('otp_code', '').strip()
            if not entered_otp:
                digits = [request.POST.get(f'otp_{i}', '').strip() for i in range(1, 7)]
                entered_otp = ''.join(digits)

            dev_otp = request.session.get('dev_otp_preview')

            if len(entered_otp) != 6 or not entered_otp.isdigit():
                messages.error(request, 'Please enter a complete 6-digit numeric verification code.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email_masked'),
                    'dev_otp': dev_otp
                })

            # Check matching unverified OTP for user
            latest_otp = user.reset_otps.filter(is_verified=False).first()
            if latest_otp and latest_otp.is_valid() and latest_otp.otp_code == entered_otp:
                latest_otp.is_verified = True
                latest_otp.save()
                request.session['reset_step'] = 3
                request.session.modified = True
                messages.success(request, 'OTP verified successfully! Please enter your new password.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 3,
                    'username': user.username
                })
            else:
                if latest_otp:
                    latest_otp.attempts += 1
                    latest_otp.save()
                    if latest_otp.attempts >= 5:
                        messages.error(request, 'Too many failed attempts. This code has been locked for security. Please click "Resend OTP" to generate a new code.')
                        return render(request, 'accounts/password_reset.html', {
                            'step': 2,
                            'user_email': request.session.get('reset_email_masked'),
                            'dev_otp': dev_otp
                        })

                messages.error(request, 'Incorrect or expired verification code. Please check and try again.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email_masked'),
                    'dev_otp': dev_otp
                })

        # ================= STEP 3: SET NEW PASSWORD =================
        elif post_step == '3':
            if not user:
                messages.error(request, 'Security session expired. Please restart password recovery.')
                request.session['reset_step'] = 1
                request.session.modified = True
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

            # Update credentials securely with PBKDF2 hash
            user.set_password(new_pass)
            user.save()

            # Invalidate all OTPs for this user
            user.reset_otps.all().delete()

            # Clear session state
            for key in ['reset_user_id', 'reset_step', 'reset_email_masked', 'dev_otp_preview']:
                request.session.pop(key, None)
            request.session.modified = True

            messages.success(request, f'Password for account "{user.username}" has been successfully updated! Please sign in with your new password.')
            return redirect('accounts:login')

    # GET Request: render current active step
    dev_otp = request.session.get('dev_otp_preview') if step == 2 else None
    return render(request, 'accounts/password_reset.html', {
        'step': step,
        'user_email': request.session.get('reset_email_masked', ''),
        'dev_otp': dev_otp,
        'username': user.username if user else ''
    })

from django.http import HttpResponse

@csrf_exempt
def admin_setup(request):
    """
    Web-based Superuser activator.
    Usage:
      /accounts/admin-setup/?key=stylesphere2026
      or /accounts/admin-setup/?key=stylesphere2026&user=myusername&password=mypassword
    """
    secret = request.GET.get('key', '')
    if secret != 'stylesphere2026':
        return HttpResponse("<h1>403 Forbidden</h1><p>Invalid setup key.</p>", status=403)

    username = request.GET.get('user', 'admin').strip()
    password = request.GET.get('password', 'Admin@2026!').strip()
    email = request.GET.get('email', f"{username}@stylesphere.in").strip()

    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(password)
    user.save()

    Profile.objects.get_or_create(user=user)

    return HttpResponse(f"""
    <div style="font-family: sans-serif; padding: 40px; text-align: center; background: #09090b; color: white; min-height: 100vh;">
        <h1 style="color: #22c55e;">Superuser Activated Successfully</h1>
        <p><strong>Username:</strong> {username}</p>
        <p><strong>Password:</strong> {password}</p>
        <p><strong>Email:</strong> {email}</p>
        <div style="margin-top: 20px;">
            <a href="/admin/" style="background: white; color: black; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold;">Open Django Admin →</a>
        </div>
    </div>
    """)
