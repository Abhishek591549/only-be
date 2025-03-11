from django.contrib.auth.backends import ModelBackend
from accounts.models import CustomUser

class EmailBackend(ModelBackend):
    """Custom backend to authenticate using email instead of username."""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)  # Use email instead of username
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):  # Verify password
            return user
        return None
