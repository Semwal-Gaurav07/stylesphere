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
        return 'your registered email'
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
    User-Centric Email & OTP Password Reset Flow:
    Step 1: Check if given email exists in database. If found, generate 6-digit OTP and send to user's Gmail.
    Step 2: User enters the 6-digit OTP code received in Gmail. Verify code.
    Step 3: User sets new password and saves to database.
    """
    if request.user.is_authenticated:
        return redirect('store:product_list')

    # Allow query parameter to restart flow
    if request.GET.get('restart'):
        for key in ['reset_user_id', 'reset_step', 'reset_email', 'reset_email_masked', 'dev_otp_preview']:
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

        # ================= STEP 1: CHECK EMAIL IN DB & DISPATCH CODE =================
        if post_step == '1':
            email_input = request.POST.get('email', '').strip().lower() or request.POST.get('identifier', '').strip().lower()
            if not email_input:
                messages.error(request, 'Please enter your registered email address.')
                return render(request, 'accounts/password_reset.html', {'step': 1})

            # 1. Look up user by email in database
            found_user = User.objects.filter(email__iexact=email_input).first()

            # Optional fallback by username if user typed username instead of email
            if not found_user:
                found_user = User.objects.filter(username__iexact=email_input).first()

            # If user is NOT found in database:
            if not found_user:
                messages.error(request, f"No account found with the email '{email_input}'. Please verify your email or register a new account.")
                return render(request, 'accounts/password_reset.html', {'step': 1, 'email_input': email_input})

            # If user has no email address on record:
            if not found_user.email:
                messages.error(request, f"Account '{found_user.username}' has no email address on file to receive verification codes. Please contact support via WhatsApp.")
                return render(request, 'accounts/password_reset.html', {'step': 1, 'email_input': email_input})

            # 2. User found in database -> Generate 6-digit OTP
            otp = PasswordResetOTP.create_otp(found_user)
            request.session['reset_user_id'] = found_user.id
            request.session['reset_step'] = 2
            request.session['reset_email'] = found_user.email
            masked = mask_email(found_user.email)
            request.session['reset_email_masked'] = masked

            # Developer / test mode preview helper
            is_dev = getattr(settings, 'DEBUG', True) or 'console' in getattr(settings, 'EMAIL_BACKEND', '').lower()
            dev_otp = otp.otp_code if is_dev else None
            request.session['dev_otp_preview'] = dev_otp or ''
            request.session.modified = True

            # Print to terminal
            print("\n" + "=" * 65)
            print(f"📧 [PASSWORD RESET VERIFICATION CODE]")
            print(f"Recipient: {found_user.email} (Username: {found_user.username})")
            print(f"6-Digit Verification Code: {otp.otp_code} | Valid for: 10 min")
            print("=" * 65 + "\n")

            # 3. Dispatch transactional email to user's Gmail
            subject = f"Your Style Sphere Verification Code: {otp.otp_code}"
            body = (
                f"Hello {found_user.first_name or found_user.username},\n\n"
                f"We received a request to reset your Style Sphere account password.\n\n"
                f"Your 6-digit verification code is:\n\n"
                f"  {otp.otp_code}\n\n"
                f"This code is valid for 10 minutes.\n"
                f"Enter this code on the verification screen to choose a new password.\n\n"
                f"If you did not request this code, you can safely ignore this email.\n\n"
                f"— Style Sphere Atelier Support\n"
                f"Panchkula, Haryana"
            )
            html_message = f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #09090b; color: #ffffff; padding: 40px 20px;">
                <div style="max-width: 520px; margin: 0 auto; background-color: #111114; border: 1px solid #27272a; border-radius: 16px; padding: 36px; text-align: center;">
                    <h1 style="color: #ffffff; font-size: 22px; font-weight: 800; letter-spacing: 0.15em; margin: 0 0 4px 0;">STYLE SPHERE</h1>
                    <div style="color: #a1a1aa; font-size: 10px; text-transform: uppercase; letter-spacing: 0.25em; margin-bottom: 24px;">Atelier de Couture</div>
                    <div style="height: 1px; background-color: #27272a; margin-bottom: 24px;"></div>
                    <h2 style="color: #ffffff; font-size: 17px; font-weight: 700; margin: 0 0 12px 0;">Password Reset Verification</h2>
                    <p style="color: #a1a1aa; font-size: 13px; line-height: 1.6; margin: 0 0 24px 0;">
                        Hello <strong style="color: #ffffff;">{found_user.first_name or found_user.username}</strong>,<br>
                        Enter the following 6-digit verification code to reset your account password:
                    </p>
                    <div style="background-color: #000000; border: 2px solid #ef4444; border-radius: 12px; padding: 18px 28px; display: inline-block; margin-bottom: 20px;">
                        <span style="color: #ef4444; font-size: 32px; font-weight: 900; letter-spacing: 0.25em; font-family: monospace;">{otp.otp_code}</span>
                    </div>
                    <p style="color: #71717a; font-size: 12px; margin: 0 0 24px 0;">
                        ⏱️ Code expires in <strong>10 minutes</strong>.
                    </p>
                    <div style="height: 1px; background-color: #27272a; margin-bottom: 20px;"></div>
                    <p style="color: #52525b; font-size: 11px; line-height: 1.5; margin: 0;">
                        If you did not request a password reset, you can safely ignore this email.
                    </p>
                </div>
            </div>
            """

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    html_message=html_message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'Style Sphere Atelier <noreply@stylesphere.in>'),
                    recipient_list=[found_user.email],
                    fail_silently=False
                )
                messages.success(request, f"Verification code sent to {found_user.email}! Please check your inbox.")
            except Exception as e:
                print(f"SMTP Email Error: {e}")
                if 'console' in getattr(settings, 'EMAIL_BACKEND', '').lower():
                    messages.info(request, f"Verification code generated for {found_user.email}. (Console mode: code is {otp.otp_code})")
                else:
                    messages.error(request, f"Could not dispatch email to {found_user.email}: {e}. Check your SMTP credentials in .env.")

            return render(request, 'accounts/password_reset.html', {
                'step': 2,
                'user_email': found_user.email,
                'dev_otp': dev_otp
            })

        # ================= STEP 2: VERIFY 6-DIGIT CODE =================
        elif post_step == '2':
            if not user:
                messages.error(request, 'Session expired. Please enter your email address again.')
                request.session['reset_step'] = 1
                request.session.modified = True
                return redirect('accounts:password_reset')

            # Resend action
            if request.POST.get('action') == 'resend':
                otp = PasswordResetOTP.create_otp(user)
                is_dev = getattr(settings, 'DEBUG', True) or 'console' in getattr(settings, 'EMAIL_BACKEND', '').lower()
                dev_otp = otp.otp_code if is_dev else None
                request.session['dev_otp_preview'] = dev_otp or ''
                request.session.modified = True

                print(f"\n🔑 [STYLE SPHERE RESENT OTP] User: {user.username} | Email: {user.email} | Code: {otp.otp_code}\n")

                try:
                    subject = f"Your New Style Sphere Verification Code: {otp.otp_code}"
                    body = f"Hello {user.username},\n\nYour new 6-digit verification code is:\n\n  {otp.otp_code}\n\nValid for 10 minutes."
                    send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@stylesphere.in'), [user.email], fail_silently=False)
                    messages.success(request, f'A fresh verification code was sent to {user.email}!')
                except Exception as e:
                    print(f"Resend error: {e}")
                    messages.info(request, f'A fresh code was generated for {user.email}. (Code: {otp.otp_code})')

                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': user.email,
                    'dev_otp': dev_otp
                })

            # Assemble 6-digit code
            entered_otp = request.POST.get('otp_code', '').strip()
            if not entered_otp:
                digits = [request.POST.get(f'otp_{i}', '').strip() for i in range(1, 7)]
                entered_otp = ''.join(digits)

            dev_otp = request.session.get('dev_otp_preview')

            if len(entered_otp) != 6 or not entered_otp.isdigit():
                messages.error(request, 'Please enter the complete 6-digit verification code sent to your email.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email', user.email),
                    'dev_otp': dev_otp
                })

            # Verify OTP in database
            latest_otp = user.reset_otps.filter(is_verified=False).first()
            if latest_otp and latest_otp.is_valid() and latest_otp.otp_code == entered_otp:
                latest_otp.is_verified = True
                latest_otp.save()
                request.session['reset_step'] = 3
                request.session.modified = True
                messages.success(request, 'Verification code verified! You can now choose your new password.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 3,
                    'username': user.username
                })
            else:
                if latest_otp:
                    latest_otp.attempts += 1
                    latest_otp.save()
                    if latest_otp.attempts >= 5:
                        messages.error(request, 'Too many incorrect attempts. This code has been expired for security. Please click "Resend OTP" to request a new code.')
                        return render(request, 'accounts/password_reset.html', {
                            'step': 2,
                            'user_email': request.session.get('reset_email', user.email),
                            'dev_otp': dev_otp
                        })

                messages.error(request, 'Invalid or expired verification code. Please check your Gmail and enter the 6-digit code again.')
                return render(request, 'accounts/password_reset.html', {
                    'step': 2,
                    'user_email': request.session.get('reset_email', user.email),
                    'dev_otp': dev_otp
                })

        # ================= STEP 3: UPDATE NEW PASSWORD =================
        elif post_step == '3':
            if not user:
                messages.error(request, 'Session expired. Please enter your email address again.')
                request.session['reset_step'] = 1
                request.session.modified = True
                return redirect('accounts:password_reset')

            new_pass = request.POST.get('new_password', '').strip()
            confirm_pass = request.POST.get('confirm_password', '').strip()

            if not new_pass or not confirm_pass:
                messages.error(request, 'Please fill in both password fields.')
                return render(request, 'accounts/password_reset.html', {'step': 3, 'username': user.username})

            if new_pass != confirm_pass:
                messages.error(request, 'Passwords do not match. Please ensure both passwords are identical.')
                return render(request, 'accounts/password_reset.html', {'step': 3, 'username': user.username})

            from django.contrib.auth.password_validation import validate_password
            from django.core.exceptions import ValidationError

            try:
                validate_password(new_pass, user=user)
            except ValidationError as e:
                for error_msg in e.messages:
                    messages.error(request, error_msg)
                return render(request, 'accounts/password_reset.html', {'step': 3, 'username': user.username})

            # Save new hashed password
            user.set_password(new_pass)
            user.save()

            # Clean up all OTP tokens for user
            user.reset_otps.all().delete()

            # Clear session
            for key in ['reset_user_id', 'reset_step', 'reset_email', 'reset_email_masked', 'dev_otp_preview']:
                request.session.pop(key, None)
            request.session.modified = True

            messages.success(request, f'Password for account "{user.username}" has been successfully updated! You can now log in with your new password.')
            return redirect('accounts:login')

    # GET Request: render current active step
    dev_otp = request.session.get('dev_otp_preview') if step == 2 else None
    return render(request, 'accounts/password_reset.html', {
        'step': step,
        'user_email': request.session.get('reset_email', user.email if user else ''),
        'dev_otp': dev_otp,
        'username': user.username if user else ''
    })
