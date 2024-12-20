# backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomBackend(ModelBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(username=username).first()
        
        if user and user.check_password(password):
            return user
