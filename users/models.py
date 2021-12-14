from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from users.validators import username_validator, birth_date_validator


class UserQuerySet(models.QuerySet):
    def staff(self) -> QuerySet['User']:
        return self.filter(type=User.Types.STAFF)

    def doctors(self) -> QuerySet['User']:
        return self.filter(type=User.Types.DOCTOR)

    def patients(self) -> QuerySet['User']:
        return self.filter(type=User.Types.PATIENT)


class UserManager(BaseUserManager):
    def create_superuser(
        self, username: str, email: str, password: str, first_name: str = "", last_name: str = ""
    ) -> "User":
        """Creates an instance of User with superuser status and saves it to the database."""
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.type = User.Types.STAFF
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, first_name: str, last_name: str, password: str, type: str
    ) -> "User":
        """Creates an instance of User without extra permissions and saves it to the database."""
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            type=type
        )
        user.save(using=self._db)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def staff(self) -> QuerySet['User']:
        return self.get_queryset().staff()

    def doctors(self) -> QuerySet['User']:
        return self.get_queryset().doctors()

    def patients(self) -> QuerySet['User']:
        return self.get_queryset().patients()


class User(AbstractUser):
    class Types(models.TextChoices):
        STAFF = "STAFF", "STAFF"
        DOCTOR = "DOCTOR", "DOCTOR"
        PATIENT = "PATIENT", "PATIENT"

    username = models.CharField(
        _('username'), max_length=150, blank=True, null=True, unique=True,
        help_text=_('Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Unique email address')
    )
    birth_date = models.DateField(_('birth date'), blank=True, null=True, validators=[birth_date_validator])
    type = models.CharField(
        _('user type'), max_length=8, choices=Types.choices
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
