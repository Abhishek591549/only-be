from django.shortcuts import render
from django.core.mail import send_mail
import json
from django.core.cache import cache

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache
from django.utils.timezone import now, timedelta
from django.contrib.auth.hashers import make_password
from .models import CustomUser

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from .models import CustomUser


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta
from .models import CustomUser  # ✅ Ensure CustomUser model is imported


import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.shortcuts import redirect
from datetime import timedelta
from .models import CustomUser


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.utils.timezone import now
from datetime import timedelta
from .models import CustomUser  # Ensure you have a CustomUser model

@csrf_exempt
def register_user_api(request):
    """API to register a new user and redirect to OTP verification."""
    if request.method == "POST":
        try:
            # ✅ Handle form data correctly
            full_name = request.POST.get("full_name")
            user_email = request.POST.get("email")
            user_address = request.POST.get("address")
            mobile_number = request.POST.get("mobile_number")
            user_password = request.POST.get("password")
            confirm_user_password = request.POST.get("confirm_password")

            # ✅ Validate required fields
            if not all([full_name, user_email, user_address, mobile_number, user_password, confirm_user_password]):
                return JsonResponse({"error": "❌ All fields are required."}, status=400)

            # ✅ Check if email is already registered
            if CustomUser.objects.filter(email=user_email, is_verified=True).exists():
                return JsonResponse({"error": "❌ Email is already registered."}, status=400)

            # ✅ Check if passwords match
            if user_password != confirm_user_password:
                return JsonResponse({"error": "❌ Passwords do not match."}, status=400)

            # ✅ Generate OTP and expiry time
            otp_code = generate_otp()
            otp_expiry_time = now() + timedelta(seconds=150)

            # ✅ Save user temporarily with OTP in cache
            cache.set(
                f"user_{user_email}",
                {
                    "full_name": full_name,
                    "email": user_email,
                    "address": user_address,
                    "mobile_number": mobile_number,
                 "password": user_password,  # ✅ Raw password (plain text for now)


                    "otp_code": otp_code,
                    "otp_expiry_time": otp_expiry_time,
                },
                timeout=300,  # Cache expires in 5 minutes
            )

            # ✅ Send OTP to user's email
            send_otp_email(user_email, otp_code)

            # ✅ Return JSON with redirect URL to the OTP verification page
            return JsonResponse({
                "message": f"✅ OTP sent to {user_email}. Redirecting...",
                "redirect_url": f"/verify-otp/?email={user_email}"
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": f"❌ An error occurred: {str(e)}"}, status=400)

    return JsonResponse({"error": "❌ Only POST method allowed."}, status=405)

from django.http import JsonResponse
from django.core.cache import cache
import json
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser  # Ensure your CustomUser model is correctly imported
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser  # Import your custom user model

import json
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.timezone import now
from .models import CustomUser  # Ensure you have imported your user model




from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser  # Import your user model

import json
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.timezone import now
from .models import CustomUser  # Ensure your model is imported

import json
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.timezone import now
from .models import CustomUser  

import json
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.timezone import now
from .models import CustomUser  
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.timezone import now
from .models import CustomUser  

from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.timezone import now
import json



from django.shortcuts import render
def home_view(request):
    return render(request, "index.html")

# ✅ Register Page (Renders the registration form)
def register_view(request):
    return render(request, "register.html")
from django.shortcuts import render
from django.http import HttpResponse

def verify_otp(request):
    """Renders the OTP verification page."""
    email = request.GET.get("email")  # ✅ Get email from URL

    if not email:
        return HttpResponse("❌ Invalid request. Email is required.", status=400)

    return render(request, "verify_otp.html", {"email": email})  # ✅ Render OTP page



# ✅ Dashboard Page
def dashboard_view(request):
    return render(request, "dashboard.html")
from django.shortcuts import redirect
from django.core.cache import cache

from django.core.mail import send_mail

import random
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta

# ✅ Generate a 6-digit random OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# ✅ Send OTP via email
def send_otp_email(email, otp_code):
    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp_code}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

@csrf_exempt
def send_otp_api(request):
    """API to send OTP via email"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get("email")

            if not user_email:
                return JsonResponse({"error": "❌ Email is required!"}, status=400)

            otp_code = generate_otp()
            otp_expiry_time = now() + timedelta(minutes=5)

            cache.set(user_email, {"otp_code": otp_code, "otp_expiry_time": otp_expiry_time}, timeout=300)  # ✅ Store OTP for 5 minutes

            send_otp_email(user_email, otp_code)

            return JsonResponse({"message": "✅ OTP sent successfully!", "email": user_email}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "❌ Invalid JSON format."}, status=400)

    return JsonResponse({"error": "❌ Only POST method allowed"}, status=405)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache
from django.utils.timezone import now
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.core.cache import cache
from accounts.models import CustomUser  # Ensure CustomUser model is correctly imported

@csrf_exempt
def verify_otp_api(request):
    """API to verify OTP and complete registration."""
    if request.method == "POST":
        try:
            # ✅ Ensure JSON format is correctly parsed
            data = json.loads(request.body.decode("utf-8"))

            user_email = data.get("email")
            otp_entered = data.get("otp_code")

            if not user_email:
                return JsonResponse({"error": "❌ Email is required!"}, status=400)

            cached_data = cache.get(f"user_{user_email}")
            if not cached_data or "otp_code" not in cached_data:
                return JsonResponse({"error": "❌ Email not found! Please request OTP again."}, status=400)

            if cached_data["otp_code"] != otp_entered:
                return JsonResponse({"error": "❌ Invalid OTP."}, status=400)

            if cached_data["otp_expiry_time"] < now():
                cache.delete(f"user_{user_email}")
                return JsonResponse({"error": "❌ OTP has expired."}, status=400)

            # ✅ Extract first and last name if available
            full_name = cached_data.get("full_name", "")
            name_parts = full_name.split()
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            # ✅ Create and save the user properly
            user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=user_email,
                email=user_email,
                address=cached_data["address"],
                mobile_number=cached_data["mobile_number"],
                is_verified=True
            )
            user.set_password(cached_data["password"])  # ✅ This will hash it correctly

            user.save()

            cache.delete(f"user_{user_email}")

            return JsonResponse({"message": "✅ OTP Verified! Redirecting to login...", "redirect_url": "/login/"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "❌ Invalid JSON format."}, status=400)

    return JsonResponse({"error": "❌ Only POST method allowed"}, status=405)

# accounts/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import json
from accounts.models import CustomUser  # import your user model

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
import json

@csrf_exempt
def login_user_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "❌ Email and password are required."}, status=400)

            try:
                user_obj = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "❌ Invalid email or password."}, status=400)

            # ✅ Authenticate using the actual username (which Django uses internally)
            user = authenticate(request, username=user_obj.username, password=password)

            if user is None:
                return JsonResponse({"error": "❌ Invalid email or password."}, status=400)

            if not user.is_verified:
                return JsonResponse({"error": "❌ Email not verified."}, status=403)

            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "message": "✅ Login successful!",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "redirect_url": "/dashboard/"
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "❌ Invalid JSON format."}, status=400)

    return JsonResponse({"error": "❌ Only POST method allowed."}, status=405)
from django.shortcuts import render

def dashboard_view(request):
    return render(request, "dashboard.html")  # Make sure you have a template for this
def logout_user(request):
    """Logs out the user and redirects to login page."""
    logout(request)  # ✅ Logs out the user
    return redirect('/login/')  # ✅ Redirect to login page
def login_page(request):
    """Render the Login Page."""
    return render(request, "login.html")
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def productspage(request):
    return render(request, "products.html")

def my_orders(request):
    return render(request, "my_orders.html")

def payment(request):
    return render(request, "payment.html")

