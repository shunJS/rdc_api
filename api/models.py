import uuid

from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_or_create_for_cognito(self, payload):
        """Get any value from `payload` here
        ipdb> pprint(payload)
        {'aud': '159ufjrihgehb67sn373aotli7',
        'auth_time': 1583503962,
        'cognito:username': 'john-rambo',
        'email': 'foggygiga@gmail.com',
        'email_verified': True,
        'event_id': 'd92a99c2-c49e-4312-8a57-c0dccb84f1c3',
        'exp': 1583507562,
        'iat': 1583503962,
        'iss': 'https://cognito-idp.us-west-2.amazonaws.com/us-west-2_flCJaoDig',
        'sub': '2e4790a0-35a4-45d7-b10c-ced79be22e94',
        'token_use': 'id'}
        """
        cognito_id = payload['sub']

        try:
            return self.get(cognito_id=cognito_id)
        except self.model.DoesNotExist:
            pass

        try:
            user = self.create(
                cognito_id=cognito_id,
                email=payload['email'],
                is_active=True)
        except IntegrityError:
            user = self.get(cognito_id=cognito_id)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    cognito_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin




class Task(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title