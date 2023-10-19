
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from product.models import Product, Option, Category, GearBox, Fuel, ParentCategory, Color, Document, Comment
from user.forms import AccountForm, ContactUsForm
from user.models import FollowersList, FriendList, Profile, Account, SearchParameters, State, SearchWords
import requests
import datetime 
import re
from django.core.paginator import Paginator
from os import makedirs, path
from django.db.models import F, Q
import funtions
from funtions import get_ip_address, substract_time_messages, sub_time
from django.contrib import messages
from django.utils.translation import gettext
from django.http import HttpResponse, Http404
import re, os, json
from ch7almachya.settings import BASE_DIR


last_year = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365)

def authenticate(request, username=None, password=None):
    try:
        user = Account.objects.get(username__iexact = username.strip())

        pwd_valid = user.check_password(password)
        if pwd_valid:     
            auth.login(request, user)       
            return user
        return None
    except :
        return None

def home(request):
    context = {
        'is_home' : True,
    }
    return render(request, "home.html", context)

def home_ajax(request):
    state_name = 'state__name_' + request.LANGUAGE_CODE
    category_name = 'category__name_' + request.LANGUAGE_CODE
    products = Product.objects.filter(created_date__gte = last_year).only('name', 'category', 'other_category','price', 'given_price', 'state', 'city', 'views', 'year', 'likes_count', 'dislikes_count', 'rating', 'image', 'exchange', 'created_date', 'id', 'user', 'slug').annotate(category_name= F(category_name), state_name = F(state_name)).values('category_name', 'other_category', 'price', 'given_price', state_name, 'city', 'views', 'year', 'likes_count', 'dislikes_count', 'rating', 'image', 'exchange', 'name', 'id', 'user', 'slug').order_by("-created_date")
    products_list = []
    products_list.append((gettext("Latest").upper(), "/search/?type=newest-first&keyword=*", list(products.distinct()[:20]), ""))

    for parent in ParentCategory.objects.all().order_by('-order') :
        country_products = products.filter(category__parent = parent)[:20]
        if country_products.count() :
            products_list.append((parent.name.upper(), reverse('category', args=[parent.slug, 'null']) + "?type=best-match", list(country_products), parent.icon.url ))
    
    
    return HttpResponse(json.dumps(products_list))

def check(request):
    if request.user.id == 1 :
        profiles = Profile.objects.all().order_by("-scoore")
        i=1
        for profile in profiles :
            profile.rank = i
            i+=1

            likes = 0.0
            dislikes = 0.0
            for product in profile.user.products.all():
                likes += product.likes.all().count()
                dislikes += product.dislikes.all().count()
            if likes == 0 and dislikes == 0:
                feedback = False
            else:
                feedback = (likes/(likes + dislikes)) * 100
                feedback = round(feedback, 1)
                feedback = str(feedback) + "%"
            
            profile.feedback = feedback
            profile.save()
        messages.success(request, 'check done')
    return redirect('settings-profile')

def check_username(request):
    text = request.GET.get('text').strip()
    cond = bool(re.match(r'^[a-zA-Z1-9_]+$|^[ابتثجحخدذرزسشصضطظعغفقكلمنهويأإؤئآىة]+$', text))
    if Account.objects.filter(username__iexact=text).exists():
        return HttpResponse('F')
    else:
        return HttpResponse('T')

def check_word(name):
    return bool(re.match(r'^[a-zA-Z]+$|^[ ابتثجحخدذرزسشصضطظعغفقكلمنهويأإؤئآىة]+$', name))

def register(request):
    if not request.user.is_authenticated:
        allStates = State.objects.all()
        allColors = Color.objects.all()
        allDocuments = Document.objects.all()
        if request.method == "POST":
            first_name = request.POST.get('first_name').strip()
            last_name = request.POST.get('last_name').strip()
            username = request.POST.get('username')
            state = request.POST.get('state')
            gender = request.POST.get('gender')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            cond_1 = check_word(first_name)          
            cond_2 = check_word(last_name)
            cond_3 = bool(re.match(r'^[a-zA-Z1-9_]+$', username)) and len(username) <= 50 and not(Account.objects.filter(username__iexact=username).exists())
            cond_5 = (len(password) >= 8) and (password == confirm_password)

            
            
            if cond_1 and cond_2 and cond_3  and cond_5 and gender and state:
                try :
                    user = Account.objects.create(
                        first_name = first_name,
                        last_name = last_name,
                        username = username,
                        email = '',
                        phone_number = ''
                    )
                except :
                    raise Http404
            
                user.set_password(password)
                user.is_active = True
                user.save()
                state = allStates.get(name = request.POST.get("state"))
                Profile.objects.create(
                    user = user,
                    gender = gender,
                    password = request.POST.get('password'),
                    state = state,
                    last_active = datetime.datetime.now(datetime.timezone.utc)
                )
                FriendList.objects.create(
                    user = user
                )
                FollowersList.objects.create(
                    user=user
                )
                search_parameters = SearchParameters.objects.create(
                    user = user,
                )
                search_parameters.states.set(allStates)
                search_parameters.fuels.set(Fuel.objects.all())
                search_parameters.gear_boxs.set(GearBox.objects.all().order_by('id'))
                search_parameters.brand = Category.objects.get(slug = "all-brands")
                search_parameters.colors.set(allColors)
                search_parameters.documents.set(allDocuments)
                search_parameters.save()
                dirs = [
                    os.path.join(BASE_DIR, f"media/users/{ user.id }/userprofile/"),
                    os.path.join(BASE_DIR, f"media/users/{ user.id }/products/"),
                    os.path.join(BASE_DIR, f"media/users/{ user.id }/userprofile_150/"),
                ]
                for dir in dirs:
                    if not path.isdir(dir):
                        makedirs(dir)
                
                auth.login(request, user)
                messages.success(request, gettext('Welcome to your profile. Please remember your username "{}"').format(username) )
                search_word, case = SearchWords.objects.get_or_create(text = f"{first_name} {last_name}".lower())
    
                if not case:
                    search_word.times += 1
                    search_word.save()
                return redirect('settings-profile')
            else :
                messages.warning(request, gettext('Something went wrong, please try to register again'))
                return(redirect('register'))
        elif request.method == "GET":
            context = {
                "form" : AccountForm,
                "states" : allStates.order_by("code"),
                    
            }
        context['title'] = gettext('Register')
        context['description'] = gettext('Register with us at ch7al machya and start selling vehicles')
        return render(request, 'register.html', context)
    else:
        return redirect(reverse('home'))

def login(request):

    if not request.user.is_authenticated:
        if not request.GET.get('POST'):
            context = {
                "title" : gettext('Login'),
                "description" : gettext('Login to your account at Ch7al machya')
            }
            return render(request, 'log in.html', context)
        else :
            username = request.GET.get("username")
            password = request.GET.get("password")
            user = authenticate(request, username = username, password=password)
            if user:
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query # gets the suffix of a url
                    params = dict(x.split("=") for x in query.split('&'))
                    if "next=" in url:
                        return redirect(params["next"])
                except:
                    pass
                messages.success(request, gettext('You are logged in.'))
                return redirect('settings-profile')
            else:
                messages.warning(request, gettext("Login Failed"))
                return redirect(reverse('login'))

    else:
        return redirect(reverse('home'))

@login_required(login_url = 'login')
def logout(request):
  dark_mode = request.session.get('dark_mode')
  auth.logout(request)
  request.session['dark_mode'] = dark_mode
  request.session['is_old_user'] = True
  
  messages.success(request, gettext("You are logged out."))
  return redirect(reverse('login'))

def get_SP(request,allStates = State.objects.all(),allFuels=Fuel.objects.all(),allGearBoxs=GearBox.objects.all(),allColors=Color.objects.all(),allDocuments=Document.objects.all()):
    if request.user.is_authenticated:
        searchparameters = request.user.searchparameters
    else:
        ip = get_ip_address(request)
        searchparameters, condition = SearchParameters.objects.get_or_create(ip = ip)
        if condition:
            searchparameters.states.set(allStates)
            searchparameters.brand = Category.objects.get(slug = "all-brands")
            searchparameters.fuels.set(allFuels)
            searchparameters.gear_boxs.set(allGearBoxs)
            searchparameters.colors.set(allColors)
            searchparameters.documents.set(allDocuments)
            searchparameters.save()
    return searchparameters

def search(request):
    
    allStates = State.objects.all()
    allOptions = Option.objects.all()
    allFuels = Fuel.objects.all()
    allGearBoxs = GearBox.objects.all().order_by('id')
    allColors = Color.objects.all()
    allDocuments = Document.objects.all()

    keyword = request.GET.get('keyword').strip()
    
    searchparameters = get_SP(request, allStates, allFuels, allGearBoxs, allColors, allDocuments)

    if request.method == "POST":
        if request.POST.get('min').strip():
            searchparameters.min_price = int(request.POST.get('min'))

        if request.POST.get('max').strip():
            searchparameters.max_price = int(request.POST.get('max'))


        if request.POST.get('max-distance').strip():   
            searchparameters.max_distence = int(request.POST.get('max-distance'))

        if request.POST.get('min-year').strip():
            searchparameters.min_year = int(request.POST.get('min-year'))

        if request.POST.get('max-year').strip():   
            searchparameters.max_year = int(request.POST.get('max-year'))
            
        if request.POST.get('min-rating').strip():   
            searchparameters.minimum_rating = int(request.POST.get('min-rating'))

        states = request.POST.getlist('states')
        searchparameters.states.set(allStates.filter(name_en__in = states))

        fuels = request.POST.getlist('fuels')
        searchparameters.fuels.set(allFuels.filter(name_en__in = fuels))

        gear_boxs = request.POST.getlist('gear_boxs')
        searchparameters.gear_boxs.set(allGearBoxs.filter(name_en__in = gear_boxs))

        colors = request.POST.getlist('colors')
        searchparameters.colors.set(allColors.filter(id__in = colors))

        documents = request.POST.getlist('documents')
        searchparameters.documents.set(allDocuments.filter(id__in = documents))



        all_options = request.POST.get("all_options")
        if all_options :
            searchparameters.all_options = True
            
        else:
            searchparameters.all_options = False
        options = request.POST.getlist('options')
        searchparameters.options.set(allOptions.filter(name_en__in = options))
        searchparameters.options_list = json.dumps(options)

        exchange = request.POST.get("exchange")
        if exchange :
            searchparameters.exchange = True
        else:
            searchparameters.exchange = False
        
        value = request.POST.get("hide_none_priced")
        if value :
            searchparameters.show_none_priced = False
        else:
            searchparameters.show_none_priced = True

        brand = request.POST.get('category').strip()
        if brand == "all_brands" :
            searchparameters.brand = Category.objects.get(slug="all-brands", parent = None)
        elif brand :
            searchparameters.brand = Category.objects.get(id=int(brand))

        if request.POST.get('used'):
            searchparameters.used = True
        else:
            searchparameters.used = False

        if request.POST.get('new'):
            searchparameters.new = True
        else:
            searchparameters.new = False

        searchparameters.save()

    search_type = request.GET.get('type')
    
    
    context = {
        'keyword' : keyword,
        'search_type' : search_type,
        'search_parameters' : searchparameters,
        'states' : allStates.order_by("order"),
        "options" : allOptions.order_by('-order'),
        'gear_boxs' : allGearBoxs,
        'fuels' : allFuels,
        'title' : keyword,
        'colors' : allColors,
        'documents' :allDocuments,
        'CB' : [],

    }
    return render(request, 'search.html', context)

def search_ajax(request):
    LC = request.LANGUAGE_CODE
    keyword = request.POST.get('keyword').strip().lower()
    search_type = request.POST.get('search_type').strip()
    products_page = request.POST.get('page')

    search_parameters = SearchParameters.objects.get(id = int(request.POST.get('SPID')))

    if len(keyword) >= 2 or keyword == "*": 
        if search_parameters.all_options :
            
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category',
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )

            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )

        else:   
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category',
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
        
        keywords = re.split(' |-', keyword)
        pointing = []
        for product in products:
            
            point = 0


            #################
            product_options_list = json.loads(product['options_list'])
            SP_options_list = json.loads(search_parameters.options_list)

            if search_parameters.options.all() :
                if not product['is_all_options'] :
                    check = all(id in product_options_list for id in SP_options_list)
                    if not check:
                        continue

            ################
            if product['price'] :
                if product['price'] < search_parameters.min_price:
                    continue
                if product['price'] > search_parameters.max_price:
                    continue

            elif product['given_price'] :
                if product['given_price'] < search_parameters.min_price:
                    continue
                if product['given_price'] > search_parameters.max_price:
                    continue
                
            elif search_parameters.show_none_priced :
                pass
            else :
                continue

            ##################
            if product['rating'] < search_parameters.minimum_rating :
                continue

            ################## filtering with search key words
            if keyword  != "*":
                product_description = product['description']
                product_name = product['name'].lower()
                product_name_splited = re.split(' |-', product_name)

                for word in keywords:
                    if word in product_name_splited:
                        point += 20

                    if word in [product['category_en'].lower(), product['category_ar'], product['other_category'].lower(), str(product['year'])] :
                        point += 15

                    if word in product_description:
                        point += 10
            else:
                point = 10

            ################ ordering th filtered products
            
            if point >= 10 :
                
                if search_type == 'best-match':
     
                    point += point * (product['views'] / 100)
                    
                    point = point * (0.01 * product['rating'] * product['rating'] + 0.5 * product['rating'] + 50 ) /100

                elif search_type == 'newest-first' :

                    point = product['id']

                elif search_type == 'most-viewed' :

                    point = product['views'] 
                                
                elif search_type == 'highest-rated' :

                    point = product['rating'] + product['views'] /100

                elif search_type == 'cheapest-first' :
                    if product['price'] :
                       point = 1/ (product['price'] + 1) 
                    elif product['given_price'] :
                        point = 1/ (product['given_price'] +1 )
                    else:
                        point = 0
                
            else:
                continue

            product['created_date'] = funtions.sub_time(request, product['created_date'])
            pointing.append((product, point))
        products = sorted(pointing, key=lambda x:x[1], reverse=True)

    else:
        products = []
    
    products = Paginator(products, 20)
    last_page = products.num_pages
    products = products.page(products_page)
    return  HttpResponse(json.dumps([list(products), products.has_next(), products.has_previous(), last_page])) 

def category(request, parent, child):
    
    allStates = State.objects.all()
    allOptions = Option.objects.all()
    allFuels = Fuel.objects.all()
    allGearBoxs = GearBox.objects.all().order_by('id')
    allColors = Color.objects.all()
    allDocuments = Document.objects.all()
    country = ParentCategory.objects.get(slug = parent)
    title = country.name.capitalize()
    CB = [country.id]
    if child != "null":
        brand = Category.objects.get(slug = child, parent = country)
        title = brand.name.capitalize()
        CB.append(brand.id)
    searchparameters = get_SP(request, allStates, allFuels, allGearBoxs, allColors, allDocuments)

    if request.method == "POST":
        if request.POST.get('min').strip():
            searchparameters.min_price = int(request.POST.get('min'))

        if request.POST.get('max').strip():
            searchparameters.max_price = int(request.POST.get('max'))


        if request.POST.get('max-distance').strip():   
            searchparameters.max_distence = int(request.POST.get('max-distance'))

        if request.POST.get('min-year').strip():
            searchparameters.min_year = int(request.POST.get('min-year'))

        if request.POST.get('max-year').strip():   
            searchparameters.max_year = int(request.POST.get('max-year'))
            
        if request.POST.get('min-rating').strip():   
            searchparameters.minimum_rating = int(request.POST.get('min-rating'))

        states = request.POST.getlist('states')
        searchparameters.states.set(allStates.filter(name_en__in = states))

        fuels = request.POST.getlist('fuels')
        searchparameters.fuels.set(allFuels.filter(name_en__in = fuels))

        gear_boxs = request.POST.getlist('gear_boxs')
        searchparameters.gear_boxs.set(allGearBoxs.filter(name_en__in = gear_boxs))

        colors = request.POST.getlist('colors')
        searchparameters.colors.set(allColors.filter(id__in = colors))

        documents = request.POST.getlist('documents')
        searchparameters.documents.set(allDocuments.filter(id__in = documents))



        all_options = request.POST.get("all_options")
        if all_options :
            searchparameters.all_options = True
            
        else:
            searchparameters.all_options = False
        options = request.POST.getlist('options')
        searchparameters.options.set(allOptions.filter(name_en__in = options))
        searchparameters.options_list = json.dumps(options)

        exchange = request.POST.get("exchange")
        if exchange :
            searchparameters.exchange = True
        else:
            searchparameters.exchange = False
        
        value = request.POST.get("hide_none_priced")
        if value :
            searchparameters.show_none_priced = False
        else:
            searchparameters.show_none_priced = True

        brand = request.POST.get('category').strip()
        if brand == "all_brands" :
            searchparameters.brand = Category.objects.get(slug="all-brands", parent = None)
        elif brand :
            searchparameters.brand = Category.objects.get(id=int(brand))

        if request.POST.get('used'):
            searchparameters.used = True
        else:
            searchparameters.used = False

        if request.POST.get('new'):
            searchparameters.new = True
        else:
            searchparameters.new = False

        searchparameters.save()

    search_type = request.GET.get('type')
    
    context = {
        'search_type' : search_type,
        'search_parameters' : searchparameters,
        'states' : allStates.order_by("order"),
        "options" : allOptions.order_by('-order'),
        'gear_boxs' : allGearBoxs,
        'fuels' : allFuels,
        'title' : title,
        'colors' : allColors,
        'documents' :allDocuments,
        'CB' : CB,
        'parent' : parent,
        'child' : child,

    }
    return render(request, 'category.html', context)

def category_ajax(request):
    LC = request.LANGUAGE_CODE
    search_type = request.POST.get('search_type')
    CB = request.POST.getlist('CB[]')
    products_page = request.POST.get('page')

    search_parameters = SearchParameters.objects.get(id = int(request.POST.get('SPID')))

    if len(CB) == 1:
        if search_parameters.all_options :
        
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                    category__parent__id = int(CB[0])
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                    category__parent__id = int(CB[0])
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )

            
        else:   
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    category__parent__id = int(CB[0])
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    category__parent__id = int(CB[0])
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
                
    else:
        if search_parameters.all_options :
            
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                    category__id = int(CB[1]),
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                    category__id = int(CB[1]),
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )

        else:   
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | Q(used = not search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    category__id = int(CB[1]),
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    category__id = int(CB[1]),
                ).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
                
    pointing = []
    for product in products:
        point = 0
        #################
        product_options_list = json.loads(product['options_list'])
        SP_options_list = json.loads(search_parameters.options_list)

        if search_parameters.options.all() :
            if not product['is_all_options'] :
                check = all(id in product_options_list for id in SP_options_list)
                if not check:
                    continue

        ################
        if product['price'] :
            if product['price'] < search_parameters.min_price:
                continue
            if product['price'] > search_parameters.max_price:
                continue

        elif product['given_price'] :
            if product['given_price'] < search_parameters.min_price:
                continue
            if product['given_price'] > search_parameters.max_price:
                continue
            
        elif search_parameters.show_none_priced :
            pass
        else :
            continue

        ##################
        if product['rating'] < search_parameters.minimum_rating :
            continue

        ################## filtering with search key words

        
        point = 10

        ################ ordering th filtered products
        if search_type == 'best-match':

            point += point * (product['views'] / 100)
            
            point = point * (0.01 * product['rating'] * product['rating'] + 0.5 * product['rating'] + 50 ) /100

        elif search_type == 'newest-first' :

            point = product['id']

        elif search_type == 'most-viewed' :

            point = product['views'] 
                        
        elif search_type == 'highest-rated' :

            point = product['rating'] + product['views'] /100

        elif search_type == 'cheapest-first' :
            if product['price'] :
                point = 1/ (product['price'] + 1) 
            elif product['given_price'] :
                point = 1/ (product['given_price'] +1 )
            else:
                point = 0
        
        
        product['created_date'] = funtions.sub_time(request, product['created_date'])
        pointing.append((product, point))
        
    products = sorted(pointing, key=lambda x:x[1], reverse=True)
    products = Paginator(products, 20)
    last_page = products.num_pages
    products = products.page(products_page)
    return  HttpResponse(json.dumps([list(products), products.has_next(), products.has_previous(), last_page])) 
    
def notifications(request):
    return render(request, 'notifications.html')

def ajax_load_notifications(request):
    request.user.notified_notifications.all().update(is_acknowleged = True)
    notifications_page = int(request.GET.get('notifications_page'))
    notifications = request.user.notified_notifications.all().order_by("-id")
    count = notifications.count()
    notifications = Paginator( notifications, 20)


    notifications = notifications.get_page(notifications_page)
    
    notifications_list = []

    for notification in notifications:
        try:
            image_url = notification.notifier.profile.picture_150.url
        except:
            image_url ="/static/images/letters/" + notification.notifier.first_name[0] + ".jpg"
        

        

        notifications_list.append(
            {
                'url' : notification.url,
                'is_seen' : notification.is_seen,
                'image_url' : image_url,
                'text' : notification.text,
                'time' : sub_time(request, notification.created_date),
                'id' : notification.id,
            }
        )
    

        
    return HttpResponse(json.dumps([notifications_list, count, notifications.has_next(), notifications.has_previous()]))

def ajax_load_notifications_messages(request):
    last_messages = request.user.last_messages.all().order_by("message__created_at")
    messages_list = []
    unseen_count = last_messages.filter(is_seen = False).count()
    if unseen_count == 0 :
        unseen_count = ""
    elif unseen_count > 99 :
        unseen_count = "99+"

    for message in last_messages:
        try:
            url = message.friend.profile.picture_150.url
        except:
            if message.friend.profile.gender == "male":
                url = "/static/images/avatars/male.png"
            else:
                url = "/static/images/avatars/female.png"
        messages_list.append(
            {
                'name' : message.friend.full_name(),
                'is_user_sender' : message.message.sender == request.user,
                'text' : message.message.text,
                'image_url' : url,
                'reciever_id' : message.friend.id,
                'is_seen' : message.is_seen,
                'time' : substract_time_messages(datetime.datetime.now(datetime.timezone.utc), message.message.created_at)
            }
        )
    

    notifications = request.user.notified_notifications.all().order_by('created_date')
    
    unseen_count_2 = notifications.filter(is_seen = False).count()
    if unseen_count_2 == 0 :
        unseen_count_2 = ""
    elif unseen_count_2 > 99 :
        unseen_count_2 = "99+"
    
    notifications_list = []
    for notification in notifications:
        try:
            image_url = notification.notifier.profile.picture_150.url
        except:
            if notification.notifier.profile.gender == "male":
                image_url ="/static/images/avatars/male.png"
            else:
                image_url = "/static/images/avatars/female.png" 

        notifications_list.append(
            {
                'url' : notification.url,
                'is_seen' : notification.is_seen,
                'image_url' : image_url,
                'name' : notification.notifier.full_name(),
                'text' : notification.text,
                'time' : notification.created_date.strftime('%d-%m-%Y %H:%M'),
                'id' : notification.id,
            }
        )
        
    return HttpResponse(json.dumps([unseen_count, messages_list, notifications_list, unseen_count_2]))

def contact_us(request):
    if request.method == "GET" :
        form = ContactUsForm
    elif request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, gettext('Your message was sent successfully'))
         
            return redirect('contact-us')            

    context = {
        "form" : form,
        "title" : gettext('Contact Us'),
        "description" : gettext('Contact our team at Ch7al machya for any information we will reply to you in less than a day')
    } 
    return render(request, 'contact_us.html', context)

def NM_count(request):
    try:
        data = [request.user.notified_notifications.filter(is_acknowleged=False).count(), request.user.last_messages.filter(is_acknowleged=False).count()]

        return HttpResponse(json.dumps(data))
    except:
        return HttpResponse(json.dumps(''))

def ajax_get_comments(request):
    index = int(request.GET.get('index'))
    if index != 0:
        comments = Comment.objects.filter(product__id = request.GET.get('product_id'), id__lt = index)
        comments_count = comments.count()
        comments = comments.order_by('-id')[:10]
    else:
        comments = Comment.objects.filter(product__id = request.GET.get('product_id'))
        comments_count = comments.count()
        comments = comments.order_by('-id')[:10]
    comments_list = []
    for comment in comments:
        try:
            comments_list.append({
                'image' : comment.user.profile.picture_150.url,
                'comment_owner_name' : comment.user.full_name(),
                'comment_owner_id' : comment.user.id,
                'text' : comment.text,
                'created_date' : sub_time(request, comment.created_date),
                'id' : comment.id,
            })
        except:
            comments_list.append({
                'image' : f"/static/images/letters/{comment.user.first_name[0]}.jpg",
                'comment_owner_name' : comment.user.full_name(),
                'comment_owner_id' : comment.user.id,
                'text' : comment.text,
                'created_date' : sub_time(request, comment.created_date),
                'id' : comment.id,
            })
    return HttpResponse(json.dumps([comments_list, comments_count > 10]))

def deactivate_dark_mode(request):
    request.session['dark_mode'] = False
    return HttpResponse('')

def activate_dark_mode(request):
    request.session['dark_mode'] = True
    return HttpResponse('')

def store_search(request):
    text = request.GET.get('text')
    search_word, case = SearchWords.objects.get_or_create(text = text.lower())
    
    if not case:
        search_word.times += 1
        search_word.save()
    return HttpResponse('')

def auto_complete_suggestions(request):
    text = request.GET.get('words').strip().lower()
    if text :
        suggesstions = list(SearchWords.objects.filter(text__icontains = text).order_by('-times')[:5].values_list('text', flat= True))
    else : 
        suggesstions = []

    return HttpResponse(json.dumps(suggesstions))

def browser_notifications(request):
    try:
        notifications = request.user.notified_notifications.filter(is_acknowleged_by_browser = False, is_acknowleged = False).order_by("-id")
        messages = request.user.last_messages.filter(is_acknowleged_by_browser = False, is_acknowleged = False).order_by("-id")
        notifications_list = []

        for notification in notifications:
            try:
                image_url = notification.notifier.profile.picture_150.url
            except:
                image_url = "/static/images/letters/" +  notification.notifier.first_name[0] + ".jpg"

            notifications_list.append(
                {
                    'title' : gettext('Notification'),
                    'url' : notification.url,
                    'image_url' : image_url,
                    'text' : notification.text,
                }
            )
        
        for notification in messages:
            try:
                image_url = notification.friend.profile.picture_150.url
            except:
                image_url = "/static/images/letters/" +  notification.friend.first_name[0] + ".jpg"

            

            notifications_list.append(
                {
                    'title' : notification.friend.full_name(),
                    'url' : '/messages/' + str(notification.friend.id),
                    'image_url' : image_url,
                    'text' : notification.message.text,
                }
            )
        
        notifications.update(is_acknowleged_by_browser = True)
        messages.update(is_acknowleged_by_browser = True)

        return HttpResponse(json.dumps(notifications_list))
    except:
        return HttpResponse(json.dumps(False))
            
    

def get_people(request):
    keywords =  re.split(' |-', request.GET.get('keyword').lower().strip())
    ids = request.GET.getlist('ids[]') or []
    users = Account.objects.filter(profile__is_company = False).exclude(id__in = ids).values('last_name', 'first_name', 'id', 'profile__picture_150', 'username').annotate(scoore = F('profile__scoore'),rank = F('profile__rank'))
    
    users_list = {}
    for user in users :
        point = 0
        if keywords[0] == user['username'].lower():
            point = 100
        else:
            for keyword in keywords:
                if keyword == user['first_name'].lower() :
                    point =+ 1
                if keyword == user['last_name'].lower():
                    point += 1
                if keyword == user['username'].lower():
                    point += 1
        
        if point > 0 :
            user['point'] = point
            if not user['profile__picture_150'] :
                user['profile__picture_150'] = f'static/images/letters/{ user["first_name"][0] }.jpg'
            else:
                user['profile__picture_150'] = 'media/' + user['profile__picture_150']
            users_list[str(user['id'])] = user


    z = sorted(users_list.values(), key=lambda x:(-x['point'],-x['scoore']))
    return HttpResponse(json.dumps( [z[:20], z.__len__() > 20] ))

def get_companies(request):
    keywords =  re.split(' |-', request.GET.get('keyword').lower().strip())
    ids = request.GET.getlist('ids[]') or []
    users = Account.objects.filter(profile__is_company = True).exclude(id__in = ids).values('last_name', 'first_name', 'id', 'profile__picture_150', 'username').annotate(scoore = F('profile__scoore'),rank = F('profile__rank'))
    users_list = {}
    for user in users :
        point = 0
        if keywords[0] == user['username'].lower():
            point = 100
        else:
            for keyword in keywords:
                if keyword == user['first_name'].lower():
                    point =+ 1
                if keyword == user['last_name'].lower():
                    point += 1
                if keyword == user['username'].lower():
                    point += 1
        
        if point > 0 :
            user['point'] = point
            if not user['profile__picture_150'] :
                user['profile__picture_150'] = f'static/images/letters/{ user["first_name"][0] }.jpg'
            else:
                user['profile__picture_150'] = 'media/' + user['profile__picture_150']
            users_list[str(user['id'])] = user


    z = sorted(users_list.values(), key=lambda x:(-x['point'],-x['scoore']))
    return HttpResponse(json.dumps( [z[:20], z.__len__() > 20] ))


def error(request, str=""):
    return render(request, 'error.html')

def simular_products(request):
    LC = request.LANGUAGE_CODE
    keyword = request.GET.get('keyword').strip().lower()
    product_id = request.GET.get('product_id').strip()

    search_parameters = get_SP(request)

    if len(keyword) >= 2 or keyword == "*": 
        if search_parameters.all_options :
            
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                ).exclude(id=product_id).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category',
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )

            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                    is_all_options = True,
                ).exclude(id=product_id).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )

        else:   
            if search_parameters.brand.parent == None:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                ).exclude(id=product_id).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category',
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
            else:
                products = Product.objects.filter(
                    Q(Q(used = search_parameters.used) | ~Q(used = search_parameters.new)),
                    category = search_parameters.brand,
                    is_available=True, 
                    created_date__gt = last_year,
                    destance__lte = search_parameters.max_distence,
                    year__range = (search_parameters.min_year, search_parameters.max_year),
                    state__in = search_parameters.states.all(),
                    color__in = search_parameters.colors.all(),
                    document__in = search_parameters.documents.all(), 
                    fuel__in = search_parameters.fuels.all(), 
                    gear_box__in = search_parameters.gear_boxs.all(),
                    exchange__in = [True, search_parameters.exchange],
                ).exclude(id=product_id).annotate(
                    category_en = F('category__name_en'),
                    category_ar= F('category__name_ar'), 
                     
                    state_name = F('state__name_' + LC), 
                    gear_box_name = F('gear_box__name_' + LC), 
                    fuel_name = F('fuel__name_' + LC), 
                ).values(
                    'is_available',
                    'slug',
                    'user',
                    'name', 
                    'image',
                    'color', 
                    'document', 
                    'fuel',
                    'gear_box', 
                    'is_all_options', 
                    'options_list', 
                    'other_category', 
                    'exchange', 
                    'used', 
                    'price', 
                    'likes_count', 'dislikes_count', 'rating',
                    'views',
                    'given_price', 
                    'destance', 
                    'year', 
                    'id', 
                    'views', 
                    'category_en', 'category_ar',
                     
                    'city',
                    'state_name', 
                    'description',
                    'gear_box_name',
                    'fuel_name',
                    'engine',
                    'created_date'
                )
        
        keywords = re.split(' |-', keyword)
        pointing = []
        for product in products:
            
            point = 0


            #################
            product_options_list = json.loads(product['options_list'])
            SP_options_list = json.loads(search_parameters.options_list)

            if search_parameters.options.all() :
                if not product['is_all_options'] :
                    check = all(id in product_options_list for id in SP_options_list)
                    if not check:
                        continue

            ################
            if product['price'] :
                if product['price'] < search_parameters.min_price:
                    continue
                if product['price'] > search_parameters.max_price:
                    continue

            elif product['given_price'] :
                if product['given_price'] < search_parameters.min_price:
                    continue
                if product['given_price'] > search_parameters.max_price:
                    continue
                
            elif search_parameters.show_none_priced :
                pass
            else :
                continue

            ##################
            if product['rating'] < search_parameters.minimum_rating :
                continue

            ################## filtering with search key words
            if keyword  != "*":
                product_description = product['description']
                product_name = product['name'].lower()
                product_name_splited = re.split(' |-', product_name)

                for word in keywords:
                    if word in product_name_splited:
                        point += 20

                    if word in [product['category_en'].lower(), product['category_ar'], product['other_category'].lower(), str(product['year'])] :
                        point += 15

                    if word in product_description:
                        point += 10
            else:
                point = 10

            ################ ordering th filtered products
            
            if point >= 10 :
                    
                point += point * (product['views'] / 100)
                
                point = point * (0.01 * product['rating'] * product['rating'] + 0.5 * product['rating'] + 50 ) /100

                    
                
            else:
                continue

            product['created_date'] = funtions.sub_time(request, product['created_date'])
            pointing.append((product, point))
        products = sorted(pointing, key=lambda x:x[1], reverse=True)

    else:
        products = []
    
    products = products[:20]
    return  HttpResponse(json.dumps([list(products)])) 
    
