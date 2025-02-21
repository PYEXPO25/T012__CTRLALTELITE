from django.contrib.auth.backends import ModelBackend
from sem.models import User  # Import your custom User model

class MobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(mobile=username)  # Authenticate via mobile
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None
