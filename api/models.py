import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomizedUserManager(UserManager):
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
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    cognito_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = CustomizedUserManager()

