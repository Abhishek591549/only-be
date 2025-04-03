# import random
# from django.core.mail import send_mail
# from django.conf import settings

# def generate_otp():
#     """Generate a 6-digit OTP."""
#     return str(random.randint(100000, 999999))

# def send_otp_email(user_email, otp_code):
#     """Send OTP to user's email."""
#     subject = "Your Email Verification OTP"
#     message = f"Your OTP for email verification is: {otp_code}. It will expire in 150 seconds."
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
#     send_mail(subject, message, email_from, recipient_list)
