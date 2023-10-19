from django.shortcuts import redirect, render, reverse
from .models import Account, Notification, MessageToAdmin
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

import json

# Create your views here.
from funtions import last_active

def profile(request, user_id):
    
    try:
        owner = Account.objects.get(id=user_id)
    except:
        return render(request, 'error.html')
    
    if request.GET.get('notification_id') :
        notification = Notification.objects.get(
            notifier = owner,
            notified= request.user,
            type="follow",
        )
        notification.is_seen = True
        notification.save()

    context = {
        'owner_id' : user_id,
        'title' : owner.full_name(),
        'description' : gettext('welcome to {} profile at Ch7al machya').format(owner.full_name())
    }
    return render(request, 'user/profile.html', context)

def ajax_profile(request, user_id):
    owner = Account.objects.get(id = user_id)
    profile = owner.profile
    try:
        context = {
            "pp" : profile.picture_150.url,
            'owner_name' : owner.full_name(),
            'owner_id': owner.id,
            'bio' : profile.bio,
            'followers_count' : owner.followers_list.followers.all().count(),
            'products_count' : owner.products.all().count(),
            'feedback' : profile.feedback,
            'rank' : '#' + str( profile.rank),
            'scoore' : profile.scoore
        }
    except:
        context = {
            "pp" : f'/static/images/letters/{ owner.first_name[0] }.jpg',
            'owner_name' : owner.full_name(),
            'owner_id': owner.id,
            'bio' : profile.bio,
            'followers_count' : owner.followers_list.followers.all().count(),
            'products_count' : owner.products.all().count(),
            'feedback' : profile.feedback,
            'rank' : '#' + str( profile.rank),
            'scoore' : profile.scoore

        }
    if request.user.is_authenticated  and request.user != owner:
        context['is_follower'] = request.user in owner.followers_list.followers.all()
    else:
        context['is_follower'] = ""
    
    return HttpResponse(json.dumps(context))

def ajax_products(request, user_id):    
    owner = Account.objects.get(id = user_id)
    index = request.GET.get('index')
    if index != "0":
        products = owner.products.filter(id__lt = index).order_by('-id')
    else:
        products = owner.products.all().order_by('-id')
        
    products_len = products.count()
    products = products[:20]

    products_list = []
    for product in products:
        try :
            products_list.append({
                'id' : product.id,
                'slug' : product.slug,
                'created_date' : product.created_date.strftime("%d/%m/%Y %H:%M"),
                'name' : f'{ product.other_category or product.category.name}' + " - " + product.name,
                'price' : product.price,
                'given_price' : product.given_price,
                'views' : product.views,
                'likes_count' : product.likes.all().count(),
                'main_image' : product.image

            })
        except :
            print(product.category, product.other_category)
    
    return HttpResponse(json.dumps([products_list, products_len > 20]))

@login_required(login_url = 'login')
def report(reqeust, user_id):
    if reqeust.method == "POST" :
        MessageToAdmin.objects.create(
            type = "report",
            sender = reqeust.user,
            text = f"reporting user{user_id}",
            language = reqeust.LANGUAGE_CODE,
        )
        messages.success(reqeust, gettext("Your Report was submited"))
        return redirect("settings-profile")
    owner = Account.objects.get(id = user_id)
    context =  {
        "owner" : owner,
        "title" : gettext('Report')}
    return render(reqeust, 'user/report.html', context)


def follow_unfollow(request, user_id):
    
    if request.method == 'POST' :
        owner = Account.objects.raw(f'SELECT {user_id} AS id')[0]
        if owner.followers_list.is_follower(request.user):
            owner.followers_list.remove_follower(request.user)
            owner.profile.scoore -= 5
            owner.profile.save()
            try:
                Notification.objects.get(
                    notifier = request.user,
                    notified = owner,
                    type = "follow",
                ).delete()
            except:
                pass
        else:
            owner.followers_list.add_follower(request.user)
            owner.profile.scoore += 5
            owner.profile.save()
            Notification.objects.create(
                notifier = request.user,
                notified = owner,
                text_en = f'"{ request.user.first_name }"' +  ' Has started following you',
                text_fr = f'"{ request.user.first_name }"' +  " A commencé à vous abonner",
                text_ar = " بدأ بمتابعتك "  + f'"{ request.user.first_name }"' ,
                type = "follow",
                url = reverse('profile', args=[str(request.user.id)])
            )
        return HttpResponse('')

