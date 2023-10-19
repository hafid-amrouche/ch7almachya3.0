
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required

from django.utils.text import slugify
from user.models import State, SearchWords, Account, Notification
from product.models import Image, Product, Category, Option, GearBox, Fuel, Color, Document
from product.forms import ProductForm
from django.contrib import messages
from PIL import Image as IM
from os import makedirs, path
from django.utils.translation import gettext
import json
import re
import os, unicodedata
from ch7almachya.settings import BASE_DIR
import urllib.request
# Create your views here.

def toNormalForm(text):
    return unicodedata.normalize("NFD", text).replace(u'\u0300', '').replace(u'\u0301', '').replace(u'\u0302', '').replace(u'\u0303', '').replace(u'\u0304', '').replace(u'\u0305', '').replace(u'\u0306', '').replace(u'\u0307', '').replace(u'\u0308', '').replace(u'\u0309', '').replace(u'\u030A', '').replace(u'\u030B', '').replace(u'\u030C', '').replace(u'\u030D', '').replace(u'\u030E', '').replace(u'\u030F', '').replace(u'\u0310', '').replace(u'\u0311', '').replace(u'\u0312', '').replace(u'\u0313', '').replace(u'\u0314', '').replace(u'\u0315', '').replace(u'\u0316', '').replace(u'\u0317', '').replace(u'\u0318', '').replace(u'\u0319', '').replace(u'\u031A', '').replace(u'\u031B', '').replace(u'\u031C', '').replace(u'\u031D', '').replace(u'\u031E', '').replace(u'\u031F', '').replace(u'\u0320', '').replace(u'\u0321', '').replace(u'\u0322', '').replace(u'\u0323', '').replace(u'\u0324', '').replace(u'\u0325', '').replace(u'\u0326', '').replace(u'\u0327', '').replace(u'\u0328', '').replace(u'\u0329', '').replace(u'\u032A', '').replace(u'\u032B', '').replace(u'\u032C', '').replace(u'\u032D', '').replace(u'\u032E', '').replace(u'\u032F', '').replace(u'\u0330', '').replace(u'\u0331', '').replace(u'\u0332', '').replace(u'\u0333', '').replace(u'\u0334', '').replace(u'\u0335', '').replace(u'\u0336', '').replace(u'\u0337', '').replace(u'\u0338', '').replace(u'\u0339', '').replace(u'\u033A', '').replace(u'\u033B', '').replace(u'\u033C', '').replace(u'\u033D', '').replace(u'\u033E', '').replace(u'\u033F', '').replace(u'\u0340', '').replace(u'\u0341', '').replace(u'\u0342', '').replace(u'\u0343', '').replace(u'\u0344', '').replace(u'\u0345', '').replace(u'\u0346', '').replace(u'\u0347', '').replace(u'\u0348', '').replace(u'\u0349', '').replace(u'\u034A', '').replace(u'\u034B', '').replace(u'\u034C', '').replace(u'\u034D', '').replace(u'\u034E', '').replace(u'\u034F', '').replace(u'\u0350', '').replace(u'\u0351', '').replace(u'\u0352', '').replace(u'\u0353', '').replace(u'\u0354', '').replace(u'\u0355', '').replace(u'\u0356', '').replace(u'\u0357', '').replace(u'\u0358', '').replace(u'\u0359', '').replace(u'\u035A', '').replace(u'\u035B', '').replace(u'\u035C', '').replace(u'\u035D', '').replace(u'\u035E', '').replace(u'\u035F', '').replace(u'\u0360', '').replace(u'\u0361', '').replace(u'\u0362', '').replace(u'\u0363', '').replace(u'\u0364', '').replace(u'\u0365', '').replace(u'\u0366', '').replace(u'\u0367', '').replace(u'\u0368', '').replace(u'\u0369', '').replace(u'\u036A', '').replace(u'\u036B', '').replace(u'\u036C', '').replace(u'\u036D', '').replace(u'\u036E', '').replace(u'\u036F', '')

@login_required(login_url = 'login')
def your_items(request):
  cond = request.user.products.all().count() > 50
  context = {
    'title' : gettext("Your items"),
    'is_over_50_post' : cond
  }
  return render(request, 'dashboard/your_items.html', context)

def your_items_ajax(request):
    owner = request.user
    index = request.GET.get('index')
    if index != "0":
        products = owner.products.filter(id__lt = index).order_by('-id')
    else:
        products = owner.products.all().order_by('-id')
        
    products_len = products.count()
    products = products[:20]

    products_list = []
    for product in products:
        try:
          products_list.append({
              'id' : product.id,
              'slug' : product.slug,
              'name' :f'{ product.other_category or product.category.name}' + " - " + product.name,
              'price' : product.price,
              'given_price' : product.given_price,
              'main_image' : product.image

          })
        except:
          pass
      
    return HttpResponse(json.dumps([products_list, products_len > 20]))

@login_required(login_url = 'login')
def saved_posts(request):
  
  context = {
    'title' : gettext("Saved posts")
  }
  return render(request, 'dashboard/saved_posts.html', context)

def saved_posts_ajax(request):
    user = request.user
    index = request.GET.get('index')
    if index != "0":
        products = user.saved_item.filter(id__lt = index).order_by('-saved_at')
    else:
        products = user.saved_item.all().order_by('-saved_at')
    products_len = products.count()
    products = products[:20]

    products_list = []
    for product in products:
        product = product.item
        try:
          products_list.append({
              'id' : product.id,
              'slug' : product.slug,
              'owner_id' : product.user.id,
              'name' :f'{ product.other_category or product.category.name}' + " - " + product.name,
              'price' : product.price,
              'given_price' : product.given_price,
              'main_image' : product.image

          })
        except:
          pass
      
    return HttpResponse(json.dumps([products_list, products_len > 20]))

def check_name(name):
  return re.match(r'^[a-zA-Z0-9 -]+$', name) and re.sub(r'\s', '', name) != ""

@login_required(login_url = 'login')
def create_item(request): 
  cond = request.user.products.all().count() > 50
  if cond :
    return redirect('home')
  print(request.POST)
  allStates = State.objects.all().order_by('code')
  allColors = Color.objects.all()
  allDocuments = Document.objects.all()
  if request.method == 'POST' : 
    product = Product()
    try :
      user = request.user
      name = request.POST.get('name').strip()

      price = request.POST.get('price').strip()
      price = int(price)
      given_price = request.POST.get('given_price').strip()
      given_price = int(given_price)

      year = request.POST.get("year").strip()
      cond_1  = year.isnumeric() and int(year) <= 2023 and int(year) >= 1900

      fuel = request.POST.get("fuel").strip()
      color_id = request.POST.get("color").strip()
      document_id = request.POST.get("document").strip()
      engine = request.POST.get('engine').strip()
      gear = request.POST.get('gear').strip()
      is_all_option = bool(request.POST.get("all_options"))
      if not is_all_option :
        options_list = request.POST.getlist('options')
      else:
        options_list = []
      options_query = Option.objects.filter(id__in = options_list)
      exchange = bool(request.POST.get('exchange'))
      distance = int(request.POST.get("distance").strip())

      phone_number = [request.POST.get('phone_number').strip(), request.POST.get('phone_number2').strip(), request.POST.get('phone_number3').strip()]
      phone_number = json.dumps(phone_number)
      state = request.POST.get('state')

      parent_name, category_name = request.POST.get("category").split("|")
      category = Category.objects.get(
        name_en=category_name,
        parent__name_en=parent_name)
      if category.name_en in ['Another brand', 'Brirish brand', 'Chinese brand', 'German brand', 'French brand', 'American brand', 'Japanese brand', 'Italian brand']:
        new_brand = request.POST.get('new-brand')
        if not check_name(new_brand):
          messages.warning(request, gettext('Problem with registring the brand'))
          raise
        else:
          product.other_category = new_brand
      if check_name(name) and cond_1 and price <= 999999 and given_price <= 999999 and distance <= 99999999:
        product.user = user 
        product.name = name
        product.category = category
        product.price = price
        product.given_price = given_price
        product.save()
        product.slug = slugify( category_name + " " + name)
        product.engine = engine
        product.year = int(year)
        product.fuel = Fuel.objects.get(name_en = fuel)
        product.color = Color.objects.get(id = int(color_id))
        product.document = Document.objects.get(id = int(document_id))
        product.gear_box = GearBox.objects.get(name_en = gear)
        product.is_all_options = is_all_option
        product.options_list = json.dumps(options_list)
        product.options.set(options_query)
        product.exchange = exchange
        product.destance = distance
        description = request.POST.get('description').strip()
        product.description = toNormalForm(description)
        product.phone_number = phone_number
        product.state = State.objects.get(id= state)
        product.city = request.POST.get('city').strip()
        product.used = request.POST.get('condition') == 'used'
        
        
        dirs = [
          os.path.join(BASE_DIR, f"media/users/{ request.user.id }/products/{ product.id }/images"),
        ]
        for dir in dirs:
            if not os.path.isdir(dir):
                makedirs(dir)

        i = 0
        images_list = ''
        for value in request.FILES.getlist('images[]'):
          if i < 20 :
            image = Image.objects.create(product=product)
            try:
              p_p = IM.open(value).convert('RGB')
              p_p.thumbnail((2048,2048))
              p_p.save(
                os.path.join(BASE_DIR, f"media/users/{ request.user.id }/products/{ product.id }/images/" +  str(image.id) + ".jpg"),
                "JPEG",
                optimize=True,
                quality=60 )
              image.image = f"users/{ request.user.id }/products/{ product.id }/images/" +  str(image.id) + ".jpg"
              image.save()
              images_list += ',' + image.image.url
              if i == 0:
                p_p.thumbnail((350,350))
                p_p.save(
                  os.path.join(BASE_DIR, f"media/users/{ request.user.id }/products/{ product.id }/main.jpg"),
                  "JPEG",
                  optimize=True,
                  quality=60 )
                product.image = f"/media/users/{ request.user.id }/products/{ product.id }/main.jpg"
                
              i+=1
            except:
              image.delete()
              if request.LANGUAGE_CODE == "en" :
                messages.warning(request, f' "{value}" could not be uploaded')
              elif request.LANGUAGE_CODE == "fr" :
                messages.warning(request, f' "{value}" pu pas être téléchargé')
              elif request.LANGUAGE_CODE == "ar" :
                messages.warning(request, f'"{value}" لا يمكن تحميل الملف')
              
        if product.images.all().count() <1 :
          messages.warning(request, gettext('Your post must have at least 1 photo'))
          raise
        product.images_list = images_list.replace(",", "", 1)
            
        product.save()
        product.user.profile.scoore += 5
        product.user.profile.save()

        
        search_word, case = SearchWords.objects.get_or_create(text = f"{product.other_category or product.category.name_en} {product.name}".lower())
    
        if not case:
            search_word.times += 1
            search_word.save()
        try:
          url = reverse('product', args=[product.user.id, product.slug, product.id])
          followers = request.user.followers_list.followers.all()
          notifications = [ Notification(
            notifier = request.user,
            notified = follower,
            type = 'leader posted',
            url = url,
            special_id = product.id,
            text_en = '"{}" has added a post'.format(request.user.full_name()),
            text_fr = '"{}" a ajouter une publication'.format(request.user.full_name()),
            text_ar = 'قد أًضاف منشور "{}" '.format(request.user.full_name()),

          ) for follower in followers ]

          Notification.objects.bulk_create(notifications)
        except:
          print('error here')
        messages.success(request, gettext('Your item was created succesfully'))
        return redirect(url)
      else:
          raise
      
    except:
      messages.warning(request, gettext('Your item was Not created'))
      try :
        if product.id :
          product.delete()
      except :
        pass
      return redirect(reverse('create-item'))
  else:
    context={
      "form" : ProductForm,
      "options" : Option.objects.all().order_by('-order'),
      "fuels" : Fuel.objects.all(),
      "gear_boxs" : GearBox.objects.all().order_by("id"),
      "states" : allStates,
      "title" : gettext('Create item'),
      "documents" : allDocuments,
      "colors" : allColors,
    }
  
  return render(request, 'dashboard/create_item.html', context)

@login_required(login_url = 'login')
def edit_item(request, product_id):
  
  allStates = State.objects.all().order_by('code')
  allColors = Color.objects.all()
  allDocuments = Document.objects.all()
  product = Product.objects.get(id = product_id)
  if request.method == "POST":
    try:
      i = product.images.all().count() 
      images_list = ''
      for value in request.FILES.getlist('images[]'):
        if i < 20 :
          image = Image.objects.create(product=product)
          try:
            p_p = IM.open(value).convert('RGB')
            p_p.thumbnail((2048,2048))
            try:
              p_p.save(
                os.path.join(BASE_DIR, f"media/users/{ request.user.id }/products/{ product.id }/images/" +  str(image.id) + ".jpg"),
                "JPEG",
                optimize=True,
                quality=60 )
              image.image = f"users/{ request.user.id }/products/{ product.id }/images/" +  str(image.id) + ".jpg"
              image.save()
              i+=1
              images_list += ',' + image.image.url
              
            except:
              image.delete()
              if request.LANGUAGE_CODE == "en" :
                messages.warning(request, f' "{value}" could not be uploaded')
              elif request.LANGUAGE_CODE == "fr" :
                messages.warning(request, f' "{value}" pu pas être téléchargé')
              elif request.LANGUAGE_CODE == "ar" :
                messages.warning(request, f'"{value}" لا يمكن تحميل الملف')
              

          except:
            image.delete()
            
            
      product.images_list += images_list
      p_p = IM.open(product.images.all()[0].image.path).convert('RGB')
      p_p.thumbnail((350,350))
      p_p.save(
        os.path.join(BASE_DIR, f"media/users/{ request.user.id }/products/{ product.id }/main.jpg"),
        "JPEG",
        optimize=True,
        quality=60 )
      product.image = f"/media/users/{ request.user.id }/products/{ product.id }/main.jpg" 


      name = request.POST.get('name').strip()

      price = request.POST.get('price').strip()
      price = int(price)
      
      given_price = request.POST.get('given_price').strip()
      given_price = int(given_price)
 

      year = request.POST.get("year").strip()
      cond_1  = year.isnumeric() and int(year) <= 2023 and int(year) >= 1900

      fuel = request.POST.get("fuel").strip()
      color_id = request.POST.get("color").strip()
      document_id = request.POST.get("document").strip()
      engine = request.POST.get('engine').strip()
      gear = request.POST.get('gear').strip()
      is_all_option = bool(request.POST.get("all_options"))
      if not is_all_option :
        options_list = request.POST.getlist('options')
        options_query = Option.objects.filter(id__in = options_list)
      else:
        options_list = []
        options_query = Option.objects.filter(id__in = options_list)
      exchange = bool(request.POST.get('exchange'))
      distance = int(request.POST.get("distance").strip())

      phone_number = [request.POST.get('phone_number').strip(), request.POST.get('phone_number2').strip(), request.POST.get('phone_number3').strip()]
      phone_number = json.dumps(phone_number)
      state = request.POST.get('state')

      parent_name, category_name = request.POST.get("category").split("|")
      category = Category.objects.get(
        name_en=category_name,
        parent__name_en=parent_name)
      
      if category.name_en in ['Another brand', 'Brirish brand', 'Chinese brand', 'German brand', 'French brand', 'American brand', 'Japanese brand', 'Italian brand']:
        new_brand = request.POST.get('new-brand')
        if not check_name(new_brand):
          messages.warning(request, gettext('Problem with registring the brand'))
          raise
        else:
          product.other_category = new_brand
      else:
         product.other_category = ""
      
      if check_name(name) and cond_1 and price <= 999999 and given_price <= 999999 and distance <= 99999999:
        try:
          SW = SearchWords.objects.get(text__iexact = product.other_category or product.category.name_en + " " + product.name)
          if SW.times > 1 :
            print('uyjfhjgfgkg')
            SW.times -= 1
            SW.save()
          else:
            SW.delete()
        except:
          pass

        product.name = name
        product.price = price
        product.given_price = given_price
        product.slug = slugify( category_name + " " + name)
        product.year = int(year)
        product.fuel = Fuel.objects.get(name_en = fuel)
        product.color = Color.objects.get(id = int(color_id))
        product.document = Document.objects.get(id = int(document_id))
        product.engine = engine
        product.gear_box = GearBox.objects.get(name_en = gear)
        product.is_all_options = is_all_option
        product.options_list = json.dumps(options_list)
        product.options.set(options_query)
        product.exchange = exchange
        
        product.destance = distance
        description = request.POST.get('description').strip()
        product.description = toNormalForm(description)
        product.phone_number = phone_number
        product.state = State.objects.get(id= state)
        product.city = request.POST.get('city').strip()
        product.used = request.POST.get('condition') == 'used'
        product.category = category
        product.save()
        product.user.profile.scoore += 5
        product.user.profile.save()

        search_word, case = SearchWords.objects.get_or_create(text = f"{product.other_category or product.category.name_en} {product.name}".lower())
        if not case:
            search_word.times += 1
            search_word.save()
        messages.success(request, gettext('Your item was updated succesfully'))
        return redirect(reverse('edit-item', args=[product_id,]))
      else:
        raise
    except:
      messages.warning(request, gettext('Your item was not updated'))
      return redirect(reverse('edit-item', args=[product_id,]))
  else:
   
    phone_numbers = json.loads(product.phone_number)
    NList = [None, None, None]
    for i  in range(3):
       if phone_numbers[i] :
          NList[i] = phone_numbers[i]
    phone_numbers = NList

    context = {
      "product" : product,
      "phone_numbers" : NList,
      "image_range" : 20 - product.images.all().count(),
      "form" : ProductForm,
      "options" : Option.objects.all().order_by('-order'),
      "fuels" : Fuel.objects.all(),
      "gear_boxs" : GearBox.objects.all().order_by("id"),
      'states' : allStates,
      "title" : gettext('Edit item'),
      "colors" : allColors,
      "documents" : allDocuments,
    }
    return render(request, 'dashboard/edit_item.html', context)

@login_required(login_url = 'login')
def delete_image(request, product_id, image_id):
  
  if request.method == "GET":
    product = request.user.products.get(id = product_id)
    if product.images.all().count() > 1 : 
      image = product.images.get(id = image_id)
      product.images_list = product.images_list.replace(image.image.url + ',', '', 1)
      product.images_list = product.images_list.replace(',' + image.image.url, '', 1)
      product.images_list = product.images_list.replace(image.image.url, '', 1)
      image.delete()
      p_p = IM.open(product.images.all()[0].image.path).convert('RGB')
      p_p.thumbnail((350,350))
      p_p.save(
        os.path.join(BASE_DIR, f"media/users/{ request.user.id }/products/{ product.id }/main.jpg"),
        "JPEG",
        optimize=True,
        quality=60)
      product.image = f"/media/users/{ request.user.id }/products/{ product.id }/main.jpg"
      product.save()
  return HttpResponse('')
  

def create_item_OK(request):
  if request.user.id == 1:
    file_content = {"data" : []}
    file = open(os.path.join(BASE_DIR, 'cars.json'))
    file_data = json.load(file)
    data = file_data['data']
    with open(os.path.join(BASE_DIR, 'cars.json') , 'w') as file:
      for car_info in data :
        try :
            link = list(car_info)[0]
            if Product.objects.filter(oxid = link):
              continue
            ann = car_info[link]
            
            product = Product()
            user = Account.objects.get(id=1)

            priceText = ann['Price']
            if priceText :
              if "Negotiable" in ann['Price']:
                  price = int(float(priceText[:-19].replace(" ", "")))
                  given_price = 0
              
              elif "Fixed" in ann['Price']:
              
                  price = int(float(priceText[:-20].replace(" ", "")))
                  given_price = 0
                
              elif "Offered" in ann['Price']:
                  price = 0
                  given_price = int(float(priceText[:-16].replace(" ", "")))
              
              else :
                price = 0
                given_price = 0

            else :
              price = 0
              given_price = 0



            exchange = ann['Exchange']
            description = ann["Car Description"]
            if description :
              description = toNormalForm(description)
            else:
              description = ""
            state__name_en = ann['State'].strip()
            city = ann['City'].strip()
            used = True
            document = ann['Documents']
            
            if document == 'Yellow card':
                document = 'yellow card'
            elif document == 'Licence' :
                document = 'mojahid licence'
            else:
                document = 'grey card'
            
            gear = ann['GearBox']
            if gear == 'Manuel' or not gear:
              gear = 'manual'

            brand = toNormalForm(ann['Brand'])
            model = ann['Model']
            engine = ann['Engine'] or ""
            year = int(ann['Year'])
            fuel = ann['Energy']
            phone_number = ann["Phone numbers"]
            
            if fuel == 'Diesel' :
                fuel = 'diesel'
            elif fuel == 'GPL':
                fuel = 'LPG'
            else:
                fuel = "gasoline"

            color = ann['Color']
            if color in ['Mouse grey', 'Manitoba grey', 'Champagne grey', 'Allu grey', 'Grey']:
                color = "grey"
            elif color == 'Silver grey':
                color = 'silver'
            elif color in ['Night blue', 'Gauloise blue']:
                color = 'navy blue'
            elif color == 'Turquoise blue':
                color = 'sky blue'
            elif color in ['Green', 'Bottle green', 'Military green', 'Pistachio green']:
                color = 'green'
            elif color in ['Brown', 'Chocolate brown', 'Honey']:
                color = 'brown'
            elif color in ['Red', 'Burgundy Red']:
                color = 'red'
            elif color in ['Mauve', 'Purple', 'Eggplant']:
                color = 'purple'
            elif color == 'Other':
                color = 'other color'
            else:
                color = color.lower()

            options = ann['Car Options']
            options_new = []
            for option in options or []:
              if option == 'ABS':
                  options_new.append('airbags')

              elif option == 'ESP':
                  options_new.append('ESP system')

              elif option == 'Electric windows':
                  options_new.append('electric windows')

              elif option == 'Sunroof':
                  options_new.append('sunroof')
              
              elif option == 'Fog lights':
                  options_new.append('fog lights')
                
              elif option == 'Electric Mirrors':
                  options_new.append('electric mirrors')
              
              elif option == 'Power Steering':
                  options_new.append('power Steering')

              elif option == 'Parking sensors':
                  options_new.append('parking radar')

              elif option == 'Autoradio CD':
                  options_new.append('CD radio')

              elif option == 'Alarm':
                  options_new.append('alarm system')
                
              elif option == 'Xenon headlights':
                  options_new.append('xenon headlights')

              elif option == 'Front LED':
                  options_new.append('day time lights')
              
              elif option == 'Alloy wheels':
                  options_new.append('alloy wheels')
            
            distance = ann['Mileage']
            if distance :
              distance = int(float(distance[:-2]))
            else :
              distance = 0
          
            try:
              category = Category.objects.get(name_en__iexact = brand)
              other_category = ""
            except:
              other_category = brand
              category = Category.objects.get(slug = 'another-brand')

            product.user = user
            product.name = model
            product.price = price
            product.given_price = given_price
            product.save()
            product.slug = slugify( category.name_en + " " + model)
            product.category = category
            product.other_category = other_category
            product.engine = engine
            product.year = year
            product.fuel = Fuel.objects.get(name_en__iexact = fuel)
            product.color = Color.objects.get(name_en__iexact = color)
            product.document = Document.objects.get(name_en__iexact = document)
            product.gear_box = GearBox.objects.get(name_en__iexact = gear)
            product.options_list = json.dumps(options_new)
            options_query = Option.objects.filter(name_en__in = options_new)
            product.options.set(options_query)
            product.exchange = exchange
            product.destance = distance
            product.description = description
            product.state = State.objects.get(name_en__iexact = state__name_en)
            product.city = city
            product.used = used
            product.oxid = link
            if phone_number :
              product.phone_number = json.dumps(phone_number)
            else:
              phone_number = "[]"

            dirs = [
                      os.path.join(BASE_DIR, f"media/users/{ 1 }/products/{ product.id }/images"),
            ]
            for dir in dirs:
                  if not os.path.isdir(dir):
                      makedirs(dir)
        
            images_list = ''
            if ann['images'] :
              main_image = ann['images'][0].replace('/1600/medias', '/400/medias', 1)
              product.image = main_image
                      
              for img in ann['images']:
                images_list += ',' +  img
              images_list = images_list.replace(",", "", 1)
              product.images_list = images_list
            
            else:
              print(link, 'ERROR IMAGES>')
              file_content['data'] = file_content['data'].append(car_info)
              continue
              
            product.save()
            
            search_word, case = SearchWords.objects.get_or_create(text = f"{product.other_category or product.category.name_en} {product.name}".lower())
            if not case:
                  search_word.times += 1
                  search_word.save()
          
        except:
          try : 
            product.delete()
            file_content['data'] = file_content['data'].append(car_info)
          except:
            pass
          pass

    with open(os.path.join(BASE_DIR, 'cars.json') , 'w') as f:
      json.dump(file_content, f)
    
  return HttpResponse('')