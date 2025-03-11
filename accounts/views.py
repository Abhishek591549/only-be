from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache
from django.utils.timezone import now, timedelta
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .utils import generate_otp, send_otp_email  
@csrf_exempt
def register_user_api(request):
    """API to register a new user and send OTP via email."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            full_name = data.get("full_name")
            user_email = data.get("user_email")
            user_address = data.get("user_address")
            mobile_number = data.get("mobile_number")
            user_password = data.get("user_password")
            confirm_user_password = data.get("confirm_user_password")

            # ✅ Validate required fields
            if not all([full_name, user_email, user_address, mobile_number, user_password, confirm_user_password]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            # ✅ Check if email is already registered (only verified users)
            if CustomUser.objects.filter(email=user_email, is_verified=True).exists():
                return JsonResponse({"error": "Email is already registered."}, status=400)

            # ✅ Check if passwords match
            if user_password != confirm_user_password:
                return JsonResponse({"error": "Passwords do not match."}, status=400)

            # ✅ Generate OTP and expiry time (valid for 150 seconds)
            otp_code = generate_otp()
            otp_expiry_time = now() + timedelta(seconds=150)

            # ✅ Store user details in cache until OTP verification
            cache.set(
                user_email,  
                {
                    "full_name": full_name,
                    "user_email": user_email,
                    "user_address": user_address,
                    "mobile_number": mobile_number,
                    "user_password": make_password(user_password),
                    "otp_code": otp_code,
                    "otp_expiry_time": otp_expiry_time,
                },
                timeout=300,  # Cache expires in 5 minutes
            )

            # ✅ Send OTP to user's email
            send_otp_email(user_email, otp_code)

            return JsonResponse({"message": "OTP sent to email. Verify to complete registration."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
@csrf_exempt
def verify_otp_api(request):
    """API to verify OTP and complete registration."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get("user_email")
            otp_entered = data.get("otp_code")

            # ✅ Retrieve cached data
            cached_data = cache.get(user_email)
            print(f"🔍 Retrieved Cache Data for {user_email}: {cached_data}")  # ✅ Debug Print

            if not cached_data:
                return JsonResponse({"error": "OTP expired or invalid."}, status=400)

            # ✅ Check if OTP is correct
            if cached_data["otp_code"] != otp_entered:
                return JsonResponse({"error": "Invalid OTP."}, status=400)

            # ✅ Check if OTP has expired
            if cached_data["otp_expiry_time"] < now():
                cache.delete(user_email)  # Remove expired OTP from cache
                return JsonResponse({"error": "OTP has expired."}, status=400)

            # ✅ Create user after OTP verification
            user = CustomUser.objects.create(
                username=cached_data["full_name"],
                email=cached_data["user_email"],
                address=cached_data["user_address"],
                mobile_number=cached_data["mobile_number"],
                password=cached_data["user_password"],  
                is_verified=True,  # Mark email as verified
            )

            # ✅ Remove OTP from cache after successful verification
            cache.delete(user_email)

            return JsonResponse({"message": "User registered successfully!", "user_id": user.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser  # Import your user model

@csrf_exempt
def login_user_api(request):
    """API for user login with email and password."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get("email")  # Change 'user_email' to 'email' for consistency
            user_password = data.get("password")

            if not user_email or not user_password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

            # ✅ Authenticate user
            user = authenticate(username=user_email, password=user_password)
            if user is None:
                return JsonResponse({"error": "Invalid email or password."}, status=400)

            if not user.is_verified:  # Ensure the user is verified
                return JsonResponse({"error": "User email is not verified."}, status=400)

            # ✅ Generate JWT Tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return JsonResponse({
                "message": "Login successful.",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
