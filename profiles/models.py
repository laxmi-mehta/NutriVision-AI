from django.contrib.auth.models import AbstractUser, BaseUserManager
from bson import ObjectId  # For generating MongoDB-compatible ObjectIds
  # Import settings for AUTH_USER_MODEL
from django.db import models
from bson.objectid import ObjectId
from django.conf import settings
from djongo import models
from django.contrib.auth.models import User


class ObjectIdField(models.Field):
    description = "Field for MongoDB ObjectId"

    def get_prep_value(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

class Post(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

    @property
    def id(self):
        return str(self._id)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = ObjectId()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.CharField(max_length=24, primary_key=True, editable=False)  # Use string for ObjectId
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=10, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def save(self, *args, **kwargs):
        if not self.pk:  # Creating a new object
            super().save(*args, **kwargs)
        else:  # Updating an existing object
            update_fields = kwargs.get('update_fields', None)
            if update_fields:
                super().save(update_fields=update_fields)
            else:
                super().save(*args, **kwargs)
                
# models.py
from django.db import models
from django.contrib.auth.models import User

from djongo import models  # Use `djongo` for MongoDB compatibility

from django.db import models
from djongo import models
from django.conf import settings

class UserProfile(models.Model):
    _id = models.ObjectIdField(primary_key=True)  # Use ObjectId as the primary key
    user_id = models.CharField(max_length=255)   # Store user ID as a string for compatibility
    first_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    activity_level = models.CharField(max_length=50)
    allergy_level = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name



from django.db import models
from django.conf import settings

class UploadedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at}"

class AdminProfile(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed password