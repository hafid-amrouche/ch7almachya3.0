
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager): #this class defines how users and superusers accounts are created
  def create_user(self, first_name="", last_name="", username="", phone_number="", email="" , password=None):
    # a user is an account instance with some obligations and editing
    # this method uses the "Account class" to create users

    
    if not username:
      raise ValueError('A username is required')



    user = self.model( # creating a user with 4 fields
      email=self.normalize_email(email),
      username=username,
      phone_number = phone_number,
      first_name=first_name,
      last_name=last_name,
      
    )
 
    user.set_password(password) # setting the password sepatelly from the other fields
    
    # after creating a user we save it to the self._db
    user.save(using=self._db)
    return user

  def create_superuser(self, first_name, last_name, username, email, password,  phone_number=""):
    # a supper user is a user with a mendatory password and all 4 authorazations 
    # this defines obligated fiedls from the superuser to create an account
    super_user = self.create_user( # creating a user with 4 fields
      email = self.normalize_email(email),
      username=username,
      password=password,
      phone_number = phone_number,
      first_name=first_name,
      last_name=last_name,
    )

    super_user.is_admin = True
    super_user.is_staff = True
    super_user.is_superadmin = True
    super_user.is_active = True

    super_user.save(using=self._db)
    return super_user

class Account(AbstractBaseUser): #this class creates users
  first_name = models.CharField(max_length=50,)
  last_name = models.CharField(max_length=50,)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=100)
  phone_number = models.CharField(max_length=50)

  #required
  date_joined= models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  is_admin = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)

  # the field that you use to login is "email" insted of "username" other than "password"
  USERNAME_FIELD = 'username'
  # fields other than the 'email' and password that should apper to you when creating a superuser
  REQUIRED_FIELDS = ['first_name', 'last_name', 'email'] 

  # the user manager class that will use this base user class
  objects = MyAccountManager()

  def full_name(self):
    return self.first_name.capitalize() + " " + self.last_name.capitalize()

  def __str__(self):
    return self.full_name()
  
  def has_perm(self, perm, obj=None): # only an admin account has 'per' permissions 
    return self.is_admin

  def has_module_perms(self, add_label): # any account has 'addlabel' permissions
    return True

class Profile(models.Model):
  user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
  state = models.ForeignKey('State', null=True, blank=True, on_delete = models.SET_NULL)
  city = models.CharField(max_length=20, default="")
  picture = models.ImageField(blank=True, null=True,)
  bio = models.TextField(default="")
  scoore = models.IntegerField(default=0)
  rank = models.IntegerField(default=0)
  feedback = models.CharField(max_length=20, default="False")
  gender = models.CharField(max_length=20, blank=True, null=True)
  email_verified = models.BooleanField(default=False)
  phone_number_verified = models.BooleanField(default=False)
  password = models.CharField(null=True, blank=True, max_length=50)
  picture_150 = models.ImageField(blank=True, null=True,)
  last_active = models.DateTimeField(blank=True, null=True,)
  count = models.IntegerField(default=0)
  email_comments = models.BooleanField(default=True)
  email_messages = models.BooleanField(default=True)
  is_company = models.BooleanField(default=False)


  def __str__(self):
    return self.user.full_name()

class Notification(models.Model):
  notifier = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
  notified = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="notified_notifications")
  type = models.CharField(max_length=20)
  url = models.TextField(default="")
  text = models.TextField()
  special_id = models.IntegerField( null=True, blank=True,)
  created_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
  is_seen = models.BooleanField(default=False)
  is_acknowleged = models.BooleanField(default=False)
  is_acknowleged_by_browser = models.BooleanField(default=False)
  is_acknowleged_by_android = models.BooleanField(default=False)

  def __str__(self):
        return str(self.type) + " | " + str(self.notifier)
  def user(self):
    try:
      return self.product.user
    except:
      return self.notified

class FriendList(models.Model):
  user = models.OneToOneField('Account', on_delete = models.CASCADE)
  friends = models.ManyToManyField('Account', related_name = 'friends', blank=True)

  def add_friend(self, account):
    if account not in self.friends.all():
      self.friends.add(account)
      self.save()
    
  def remove_friend(self, account):
    if account in self.friends.all():
      self.friends.remove(account)
      self.save()

class LastMessage(models.Model):
  user = models.ForeignKey('Account', on_delete = models.CASCADE, related_name="last_messages")
  message = models.ForeignKey('message.Message', on_delete = models.CASCADE, blank=True, null=True)
  friend = models.ForeignKey('Account', on_delete = models.CASCADE, blank=True, null=True)
  is_seen = models.BooleanField(default=False)
  is_acknowleged = models.BooleanField(default=False)
  is_acknowleged_by_browser = models.BooleanField(default=False)
  is_acknowleged_by_android = models.BooleanField(default=False)

class FollowersList(models.Model):
  user = models.OneToOneField('Account', on_delete = models.CASCADE, related_name = "followers_list")
  followers = models.ManyToManyField('Account', blank=True)

  def add_follower(self, account):
    if self.followers.all():
      if account not in self.followers.all():
        self.followers.add(account)
    else:
      self.followers.add(account)  
    
  def remove_follower(self, account):
    if account in self.followers.all():
      self.followers.remove(account)
      self.save()
    
  def is_follower(self, account):
    if self.followers:
      return account in self.followers.all()
    else:
      return False

class State(models.Model):
  code = models.CharField(null=True, max_length=3)
  name = models.CharField(max_length=20, default="")
  order = models.IntegerField(null=True, blank=True)

  def __str__(self):
    return str(self.code) + " " + self.name

class SearchParameters(models.Model):
  user = models.OneToOneField('Account', on_delete=models.CASCADE, null=True, blank=True)
  ip = models.CharField(max_length=50, null=True, blank=True)
  min_price = models.IntegerField(default=0)
  max_price = models.IntegerField(default=999999)
  min_distence = models.IntegerField(default=0)
  max_distence = models.IntegerField(default=99999999)
  show_none_priced = models.BooleanField(default=True)

  min_year = models.IntegerField(default=1900)
  max_year = models.IntegerField(default=2023)

  minimum_rating = models.IntegerField(default=0)
  states = models.ManyToManyField('State')
  options = models.ManyToManyField('product.Option')
  options_list = models.TextField(default='[]')
  used = models.BooleanField(default=True)
  new= models.BooleanField(default=True)
  brand = models.ForeignKey('product.Category', null=True, on_delete=models.SET_NULL)
  all_options = models.BooleanField(default=False)

  colors = models.ManyToManyField("product.Color")
  documents = models.ManyToManyField("product.Document")

  fuels = models.ManyToManyField('product.Fuel')
  gear_boxs = models.ManyToManyField('product.GearBox')
  exchange = models.BooleanField(default=False)
  
class MessageToAdmin(models.Model):
  type = models.CharField(max_length=50)
  sender = models.ForeignKey("Account", on_delete=models.CASCADE)
  subject = models.CharField(max_length=50, null=True, blank=True)
  text = models.TextField(null=True, blank=True)
  language = models.CharField(max_length=2)
  created_date = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return str(self.sender) + " | " + str(self.created_date)

class ContactUS(models.Model):
  email = models.EmailField()
  subject = models.CharField(max_length=50, null=True, blank=True)
  text = models.TextField(max_length=1000)
  created_date = models.DateTimeField(auto_now_add=True)
  
class SearchWords(models.Model):
  text = models.CharField(max_length=50)
  times = models.IntegerField(default=1)


class SavedItem(models.Model):
  user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='saved_item')
  item = models.ForeignKey('product.Product', on_delete=models.CASCADE)
  saved_at = models.DateTimeField(auto_now=True)




