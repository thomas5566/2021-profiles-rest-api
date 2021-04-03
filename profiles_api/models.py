from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
  """Manager for user profiles"""

  def create_user(self, email, name, password=None):
    """Create a new user profile"""
    if not email:
      raise ValueError('User must have an email address')

    email = self.normalize_email(email)
    user = self.model(email=email, name=name)

    user.set_password(password)
    user.save(using=self._db) # standard django procedure for saving objects

    return user

  def create_superuser(self, email, name, password):
    """Create and save a new superuser with given detial"""
    user = self.create_user(email, name, password) # 因為create_user已經傳入self了 這邊就不用在傳入self
    
    user.is_superuser = True # is_superuser automatically created by PermissionsMixin
    user.is_staff = True # is_staff automatically created by PermissionsMixi
    user.save(using=self._db)

    return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
  """Database model for users in the system"""
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserProfileManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name']

  def get_full_name(self):
    """Retrieve full name of user"""
    return self.name
  
  def get_short_name(self):
    """Retrieve short name of user"""
    return self.name

  def __str__(self):
    """Return string repersentation of our user"""
    return self.email
