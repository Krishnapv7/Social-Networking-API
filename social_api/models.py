from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
    
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError(('The Password field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
