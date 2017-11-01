from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class EmailModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # Try to find a user matching your username
            user = User.objects.get(email=username)

            return user
        except User.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None