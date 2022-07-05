from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("First Name is required")
        if not last_name:
            raise ValueError("Last Name is required")
        if not phone:
            raise ValueError("Phone Number is required")
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user




    def create_superuser(self, email, first_name, last_name, phone, password=None):

        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.staff = True
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user






class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    confirmed_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = MyUserManager()

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin







class fplUser(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    referrer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='referred')
    fav_club = models.CharField(max_length=100, verbose_name='Favorite Club')
    total_points = models.IntegerField(default=0)
    total_referrals = models.IntegerField(default=0)
    refer_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.full_name()

    def get_referred(self):
        return fplUser.objects.filter(referrer=self, refer_valid=True)
    
    def get_referred_num(self):
        self.total_referrals = fplUser.objects.filter(referrer=self, refer_valid=True).count()
        super().save()

        

