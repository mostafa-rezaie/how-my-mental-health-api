from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, gender, password=None):
        if not email:
            raise ValueError('users must have email')
        if not username:
            raise ValueError('users must have username')
        if not gender:
            raise ValueError('users must have gender specific')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, gender, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            gender=gender,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_UNKNOWN = 'U'
    GENDER_CHOICE = ((GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_UNKNOWN, 'Unknown'))

    email = models.CharField(max_length=64, verbose_name='email', unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date-joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last-login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, null=False)
    date_of_birth = models.DateField(verbose_name='date-of-birth', null=True, blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'gender']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
