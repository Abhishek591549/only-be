from django.urls import path
from .views import register_user_api , verify_otp_api,login_user_api

urlpatterns = [
   path('register/', register_user_api, name='api-register'),  
    path('verify-otp/', verify_otp_api, name='verify-otp-api'),
      path('api/login/', login_user_api, name='api-login'),
]
