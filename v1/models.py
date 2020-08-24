from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from pagameapi1 import settings

class MyProfileManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, phone, address, birth_date, password=None, 
                    is_admin=False, is_staff=False, is_active=True, is_superuser=False):
        if not email:
            raise ValueError("Users must have an email.")
        if not username:
            raise ValueError("Users must have a username.")
        if not password:
            raise ValueError("Users must have a password.")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            
        )

        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.phone = phone
        user.birth_date = birth_date
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.superuser = is_superuser
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, phone, password, address=None, birth_date=None, **kwargs):
        user = self.create_user(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            address = address,
            birth_date = birth_date,
            password = password,
            is_superuser = True,
            is_staff = True,
            is_admin = True,
        )
        
        user.save(using=self._db)
        return user

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Profile(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=30, unique=True, default='DEFUALT USERNAME')
    email = models.EmailField(max_length=50, unique=True, default='DEFUALT EMAIL')
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30, blank=True, unique=True)
    address = models.CharField(max_length=50, blank=True, default='DEFAULT ADDRESS')
    birth_date = models.DateField(null=True, blank=True, default='DEFAULT BIRTHDAY')
    #prof_pic = models.ImageField(upload_to='profile-pics/%Y/%m/%d/')

    active = models.BooleanField(default=True, null=False)
    admin = models.BooleanField(default=False, null=False)
    staff = models.BooleanField(default=False, null=False)
    superuser = models.BooleanField(default=False, null=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'email', 'first_name', 'last_name', 'address', 'birth_date']

    objects = MyProfileManager()

    def __str__(self):
        return "email: " + self.email + ", and username: " + self.username

    def has_perms(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    @property
    def is_superuser(self):
        "Is the user active?"
        return self.superuser

    # @superuser.setter
    # def superuser(self, value):
    #     'setting super'
    #     self.superuser = value

    # @admin.setter
    # def admin(self, value):
    #     'setting admin'
    #     self.admin = value

    # @active.setter
    # def active(self, value):
    #     'setting active'
    #     self.active = value

    # @staff.setter
    # def staff(self, value):
    #     'setting staff'
    #     self.staff = value


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Transaction(models.Model):

    class StatusOptions(models.TextChoices):
        INCOMPLETE = '1', "INCOMPLETE"
        PENDING = '2', "PENDING"
        CANCELLED = '3', "CANCELLED"
        COMPLETE = '4', "COMPLETE"

    initiator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="initiator")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="recipient")
    init_timestamp = models.DateTimeField(auto_now_add=True)
    last_timestamp = models.DateTimeField(auto_now=True)
    actiontype = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=StatusOptions.choices, default=StatusOptions.PENDING)

class Account(models.Model):
  
    class AccountProvider(models.TextChoices):
        BNB = '1', "BANCO NACIONAL BOLIVIA"
        TIGO = '2', "TIGO MONEY"

    class AccountStatus(models.TextChoices):
        ACTIVE_UNV = '1', "ACTIVE UNVERIFIED"
        ACTIVE_VER = '2', "ACTIVE VERIFIED"
        INACTIVE = '3', "INACTIVE"

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, choices=AccountProvider.choices)
    status = models.CharField(max_length=20, choices=AccountStatus.choices, default=AccountStatus.ACTIVE_UNV)
    balance = models.DecimalField(max_digits=18, decimal_places=2)
