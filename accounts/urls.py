from django.urls import path
from .views import (
    home_view, register_view, register_user_api,
     verify_otp_api,
    
    dashboard_view,send_otp_email,send_otp_api, verify_otp,  dashboard_view, logout_user,login_page,logout_user,login_user_api

)
from . import views

urlpatterns = [
    path("", home_view, name="home"),  # ✅ Home Page
    path("register/", register_view, name="register"),  # ✅ Render register.html (GET)
    path("register/api/", register_user_api, name="api-register"),  # ✅ API for Registration
     path("send-otp/api/", send_otp_api, name="api-send-otp"),  
    path("verify-otp/api/", verify_otp_api, name="api-verify-otp"),
 # ✅ Render login page
     # ✅ API for login
    # ✅ User Dashboard
    path("send-otp/", send_otp_email, name="send_otp_email"), 
    path("send-otp/", send_otp_api, name="send_otp_api"),
    path("verify-otp/", verify_otp, name="verify-otp"),

      path("login/", login_page, name="login_page"),  # ✅ Login Page
     path('api/login/', login_user_api, name='login_api'),

     path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", logout_user, name="logout"),  # ✅ Logout
        path("about/", views.about, name="about"),  # About Page
    path("contact/", views.contact, name="contact"),  # Contact Page
    path("products/", views.productspage, name="productspage"),  # Products Page
   


]
