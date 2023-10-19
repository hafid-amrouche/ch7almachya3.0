from django.shortcuts import render, redirect, reverse
from user.models import Account, Notification, SavedItem
from .models import Product
from .models import Like, Dislike, Comment
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext
from django.http import HttpResponse
from funtions import sub_time
import json
from django.db.models import Q, F
import datetime, re, funtions

last_year = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365)

def save_product(request, user_id, slug, product_id):
    product = Product.objects.get(id=product_id)
    SavedItem.objects.get_or_create(
        user = request.user,
        item = product
        )
    return HttpResponse('')

def unsave_product(request, user_id, slug, product_id):
    try:
        product = Product.objects.get(id=product_id)
        SavedItem.objects.get(
            user = request.user,
            item=product
        ).delete()
    except:
        pass
    return HttpResponse('')


def product(request, user_id, slug, product_id):    
    try :
        owner = Account.objects.get(id=user_id)
        product = owner.products.get(id=product_id, slug=slug)
    except :
        return render(request, 'error.html')
    
    try:
        notifiction = Notification.objects.get(
            notified = request.user, 
            notifier = owner,
            type = 'leader posted',
            special_id = product_id
            )
        
        notifiction.is_seen = True
        notifiction.save()
        
    except:
        pass

    if owner != request.user:
        product.views += 1
        product.save()
    else:
        if request.GET.get('notification_id'):
            notifications = request.user.notified_notifications.filter(Q (Q(id = request.GET.get('notification_id')) | Q(Q(special_id = product_id))) )
            notifications.update(is_seen = True)
   

    context = {
        "product_id" : product_id,
        "user_id" : request.user.id,
        "edit_item_link" : reverse('edit-item', args=[product.id,]),
        "product_owner_id" : user_id,
        'title' : product.category.name + " - " + product.name,
        'keyword' : product.category.name_en.lower() + " " + product.name.lower(),
        'description' : gettext('{} is selling a {} {}').format(owner.full_name(), product.category.name, product.name)
    }
    return render(request, 'product/product.html', context)

def ajax_single_comment(request, user_id, slug, product_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    try:
        comment_info = {
            'image' : comment.user.profile.picture_150.url,
            'comment_owner_name' : comment.user.full_name(),
            'comment_owner_id' : comment.user.id,
            'text' : comment.text,
            'created_date' : sub_time(request, comment.created_date),
            'id' : comment.id,
            'product_owner_id' : comment.product.user.id
        }
    except:
        comment_info = {
            'image' : f"/static/images/letters/{ comment.user.first_name[0] }.jpg",
            'comment_owner_name' : comment.user.full_name(),
            'comment_owner_id' : comment.user.id,
            'text' : comment.text,
            'created_date' : sub_time(request, comment.created_date),
            'id' : comment.id,
            'product_owner_id' : comment.product.user.id
        }
    return HttpResponse(json.dumps(comment_info))

def single_comment(request, user_id, slug, product_id, comment_id):
    return render(request, 'product/single_comment.html')

def product_ajax(request):
    product = Product.objects.get(id=request.GET.get('product_id'))
    context = {
        "full_name" : product.user.full_name(),
        'time' : product.created_date.strftime("%d/%m/%Y %H:%M"),
        'images' : product.images_list.split(','),
        'likes_count' : product.likes_count,
        'dislikes_count' : product.dislikes_count,
        'phone_number' : json.loads(product.phone_number),
        'brand' :  product.other_category.capitalize() or product.category.name.capitalize(),
        'model' : product.name.capitalize(),
        'year' : product.year,
        'used' : product.used,
        'color' : product.color.name.capitalize(),
        'document' : product.document.name.capitalize(),
        'engine' : product.engine,
        'state' : product.used,
        'price' : product.price,
        'offered_price' : product.given_price,
        'exchange' : product.exchange,
        'distance' : product.destance,
        'fuel' : product.fuel.name.capitalize(),
        'gear_box' : product.gear_box.name.capitalize(),
        'all_option' : product.is_all_options,
        'state' : product.state.name.capitalize(),
        'city' : product.city.capitalize(),
        'options' : list(product.options.values_list('name')),
        'description' : product.description,
        }
    if request.user.is_authenticated :
        context['saved']  =  SavedItem.objects.filter(user = request.user,item=product).exists()
    try:
        request.user.likes.get(product=product)
        context['liked'] = True
        context['disliked'] = False
    except:
        try:
                request.user.dislikes.get(product=product)
                context['liked'] = False
                context['disliked'] = True
        except:
            context['liked'] = False
            context['disliked'] = False

   
    try :
        context['pp'] = product.user.profile.picture_150.url
    except:
         context['pp'] = f"/static/images/letters/{ product.user.first_name[0] }.jpg"
    

    return HttpResponse(json.dumps(context))

@login_required(login_url = 'login')
def delete_product(request, user_id, slug ,product_id):   
    try:
        product = request.user.products.get(id=product_id)
        product.delete()
        product.user.profile.scoore -= 5
        product.user.profile.save()
    except:
        pass
    return redirect('your-items')

@login_required(login_url = 'login')
def like(request, user_id, slug, product_id):
    
    if request.method == "POST" :
        owner = Account.objects.get(id=user_id)
        product = owner.products.get(id=product_id)
        try:
            like = request.user.likes.get(product=product)
            like.delete()

            likes_count = product.likes.all().count()
            dislikes_count = product.dislikes.all().count()
            product.likes_count = likes_count
            product.dislikes_count = dislikes_count
            try:
                product.rating = likes_count / (likes_count + dislikes_count)
            except:
                pass
    

            product.save()
            try :
                notification = request.user.notifications.get(
                    type="like",
                    special_id = product.id
                )
                notification.delete()
            except:
                pass
        except:
            try: 
                dislike = request.user.dislikes.get(product=product)
                dislike.delete()

                likes_count = product.likes.all().count()
                dislikes_count = product.dislikes.all().count()
                product.likes_count = likes_count
                product.dislikes_count = dislikes_count
                try:
                    product.rating = likes_count / (likes_count + dislikes_count)
                except:
                    pass

                product.save()
                try :
                    notification = request.user.notifications.get(
                        type="dislike",
                        special_id = product.id
                    )
                    notification.delete()
                except:
                    pass
            except:
                pass
            like = Like.objects.create(
                product=product,
                user = request.user
            )

            likes_count = product.likes.all().count()
            dislikes_count = product.dislikes.all().count()
            product.likes_count = likes_count
            product.dislikes_count = dislikes_count
            try:
                product.rating = likes_count / (likes_count + dislikes_count)
            except:
                pass

            product.save()

            product.user.profile.scoore += 2
            product.user.profile.save()
            if like.user != product.user:
                Notification.objects.create(
                    notifier = request.user,
                    notified = product.user,
                    special_id = product.id,
                    type="like",
                    text_en = f'"{request.user.first_name.upper()}" has liked your item',
                    text_fr = f'"{request.user.first_name.upper()}" a aimé votre article',
                    text_ar = f'"{request.user.first_name.upper()}" أعجبه منشوركك',
                    url = reverse('product', args=[product.user.id, product.slug, product.id]),
                )
    return HttpResponse()

@login_required(login_url = 'login')
def dislike(request, user_id, slug, product_id):
    
    if request.method == "POST" :
        owner = Account.objects.get(id=user_id)
        product = owner.products.get(id=product_id)
        try:
            dislike = request.user.dislikes.get(product=product)
            dislike.delete()

            likes_count = product.likes.all().count()
            dislikes_count = product.dislikes.all().count()
            product.likes_count = likes_count
            product.dislikes_count = dislikes_count
            try:
                product.rating = likes_count / (likes_count + dislikes_count)
            except:
                pass

            product.save()
            try :
                notification = request.user.notifications.get(
                    type="dislike",
                    special_id = product.id
                )
                notification.delete()
            except:
                pass
        except:
            try: 
                like = request.user.likes.get(product=product)
                like.delete()

                likes_count = product.likes.all().count()
                dislikes_count = product.dislikes.all().count()
                product.likes_count = likes_count
                product.dislikes_count = dislikes_count
                try:
                    product.rating = likes_count / (likes_count + dislikes_count)
                except:
                    pass

                product.save()
                try :
                    notification = request.user.notifications.get(
                        type="like",
                        special_id = product.id
                    )
                    notification.delete()
                except:
                    pass
            except:
                pass
            dislike = Dislike.objects.create(
                product=product,
                user = request.user
            )

            likes_count = product.likes.all().count()
            dislikes_count = product.dislikes.all().count()
            product.likes_count = likes_count
            product.dislikes_count = dislikes_count
            try:
                product.rating = likes_count / (likes_count + dislikes_count)
            except:
                pass

            product.save()

            product.user.profile.scoore += 2
            product.user.profile.save()
            if dislike.user != product.user:
                Notification.objects.create(
                    notifier = request.user,
                    notified = product.user,
                    special_id = product.id,
                    type="dislike",
                    text_en = f'"{ request.user.first_name.upper() }" has disliked your item',
                    text_fr = f'"{ request.user.first_name.upper() }"' + "n'a pas aimé votre article",
                    text_ar = f'"{ request.user.first_name.upper() }" لم يهجبه منشوركك',
                    url = reverse('product', args=[product.user.id, product.slug, product.id]),
                )
    return HttpResponse()

@login_required(login_url = 'login')
def comment(request, user_id, slug, product_id):
    
    owner = Account.objects.get(id=user_id)
    if request.method == 'POST' :
        if request.POST.get('comment').strip():
            product = owner.products.get(id=product_id)
            text = request.POST.get("comment").strip()
            comment = Comment.objects.create(
                product = product,
                user = request.user,
                text = text
            )
            product.user.profile.scoore += 1
            product.user.profile.save()
            if comment.user != product.user:

                Notification.objects.create(
                    notifier= request.user,
                    notified = product.user,
                    special_id = comment.id,
                    type="comment",
                    text_en = f'"{ request.user.first_name.upper() }"' + "has commented your item",
                    text_fr = f'"{ request.user.first_name.upper() }"' + "a commenté votre article",
                    text_ar = f'"{ request.user.first_name.upper() }"' + "علق على منشوركك",
                    url = reverse('product', args=[product.user.id, product.slug, product.id])
                )
                


           
            return HttpResponse(json.dumps(comment.id))
    return HttpResponse('')

@login_required(login_url = 'login')
def delete_comment(request):
    
    comment = Comment.objects.get(id=request.GET.get('comment_id'))
    comment_owner = comment.user
    product_owner = comment.product.user
    if comment_owner == request.user or product_owner == request.user:
        try:
            comment.delete()
            product_owner.profile.scoore -= 1
            product_owner.profile.save()
            try :
                notification = Notification.objects.get(
                type="comment",
                special_id = comment.id,
                )
                notification.delete()
            except:
                pass
            
        except:
            pass
    return HttpResponse()