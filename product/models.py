from django.db import models
# Create your models here.


class ParentCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="")
    order = models.IntegerField(null=True, blank=True)
    icon = models.ImageField(null=True, blank=True, upload_to='countries_flags/')


    def __str__(self):
        return self.name_en

class Category(models.Model):
    parent = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, related_name="children", null=True, blank=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="")
    order = models.IntegerField(default=0, blank=True)
    icon = models.ImageField(null=True, blank=True, upload_to='brands_flags/')

    def __str__(self):
        return self.name_en

class Product(models.Model):
    user = models.ForeignKey('user.Account', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, null=True, blank=True)
    other_category = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="slug")
    price = models.IntegerField(null=True, blank=True)
    engine = models.CharField(max_length=30, default="")
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True)
    given_price = models.IntegerField(null=True, blank=True)
    images_list = models.TextField(default="")
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=50)
    used = models.BooleanField(default=True)
    image = models.TextField(default="")
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    exchange = models.BooleanField(default=False)
    year = models.IntegerField(default=1900)
    views = models.IntegerField(default=0)
    fuel = models.ForeignKey('Fuel', null=True, on_delete=models.SET_NULL)
    gear_box = models.ForeignKey('GearBox', null=True, on_delete=models.SET_NULL)
    is_all_options = models.BooleanField(default=False)
    options = models.ManyToManyField('Option')
    options_list = models.TextField(default="[]")
    destance = models.IntegerField(default=999999999)
    phone_number = models.TextField(default="")
    state = models.ForeignKey('user.State', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    oxid = models.TextField(default = "")



    def __str__(self):
        return self.name
        
class Color(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) :
        return self.name

class Document(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) :
        return self.name

class Detail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length = 50)
    text = models.TextField()
    def __str__(self):
        return self.title

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()

    def __str__(self):
        try:
            return self.image.url
        except:
            return self.product.name

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('user.Account', on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Dislike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey('user.Account', on_delete=models.CASCADE, related_name='dislikes')
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('user.Account', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return str(self.product) + " | " + str(self.user)

class Option(models.Model):
    name = models.CharField(max_length=30, null=True)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Fuel(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class GearBox(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    


    