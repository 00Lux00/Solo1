from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.data import COUNTRIES
from django.db.models import Q, F
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    avatar = models.ImageField(default='defaultimages/default.jpeg', upload_to='avatar',null=True, blank=True)
    about = models.CharField(max_length=160, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    activation_code = models.CharField(max_length=255, blank=True)
    followers = models.ManyToManyField('self', related_name='followers', blank=True)
    followings = models.ManyToManyField('self', related_name='followings', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'@{self.username}'

    def create_activation_code(self):
        import hashlib
        string = self.email + self.email
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception('Code is invalid')
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    @property
    def post_count(self):
        return self.post.all().count()






    #class user 4-th point
    # header = models.ImageField(default='defaultimages/defaultcover.png', upload_to='headers', blank=True, null=True)
