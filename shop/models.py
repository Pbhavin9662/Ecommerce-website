from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ShippingAddress(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    address1 = models.CharField(max_length=150, default='0',null=True)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=50,default='0', null=True)
    state = models.CharField(max_length=50, default='0',null=True)
    zipcode = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=5, default='IND', null=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return str(self.address1) if self.address1 else ''

class BillingAddress(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    username =  models.CharField(max_length=100,default='0',null=True)
    mobile = models.CharField(max_length=100,default='0',null=True)
    email = models.EmailField(max_length=100,default="xyz123@gmail.com")
    country = models.CharField(max_length=7, default='INDIA', null=False)
    address1 = models.CharField(max_length=150, null=True,default='0')
    address2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=50,default='0', null=True)
    state = models.CharField(max_length=50,default='0', null=True)
    zipcode = models.CharField(max_length=10,default='0', null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return str(self.address1) if self.address1 else ''



class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=20, default=0)
    alternate_mobile_no = models.CharField(
        max_length=20, default="0", null=True)
    addresses = models.ManyToManyField(ShippingAddress)
    profile_image = models.ImageField(default='basicpic.png', null=True, blank=True)

    def __str__(self):
        return str(self.account)




# product models
class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ('-created_at',)


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)

    @staticmethod
    def get_all_scproducts():
        return Category.objects.all()

    @staticmethod
    def get_all_SubCategory_By_Categoryid(sc_id):
        if sc_id:
            return SubCategory.objects.filter(category=sc_id)
        else:
            return SubCategory.get_all_scproducts();

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, null=True, default="xyz")
    category = models.ForeignKey(
    Category, on_delete=models.SET_NULL, default="xyz", null=True)
    subcategory = models.ForeignKey(
    SubCategory, on_delete=models.SET_NULL, default="xyz", null=True)
    brand = models.ForeignKey(
    Brand, on_delete=models.CASCADE, null=True, default="xyz")
    product_image = models.ImageField(upload_to="", default='cart.jpg', null=True, blank=True)
    price = models.CharField(max_length=50, null=True, default=000)
    description = models.TextField(max_length=5000, null=True, default="this is Default Product...")
   
    @staticmethod
    def get_all_scproducts():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_Subcategory(val):
        if val:
            return Product.objects.filter(subcategory=val)
        else:
            return Product.get_all_scproducts();

    def __str__(self):
        return self.name


class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    trasaction_id = models.CharField(max_length=100, null=True,unique=True)

    def __str__(self):
        return str(self.account)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        price = int(self.product.price)
        total = price * self.quantity
        return total
    def __str__(self):
        return str(self.id)