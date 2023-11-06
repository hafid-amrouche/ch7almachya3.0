from django.shortcuts import redirect, render
from .models import Message
from user.models import Account
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from funtions import last_active
from django.utils.translation import gettext
from django.http import Http404, HttpResponse
import json
from ch7almachya.user_interface_RT_updating import update_NMCount
# Create your views here.
 
@login_required(login_url = 'login')
def messages_list(request):
    last_active(request)
    return render(request, 'message/messages_list.html')

@login_required(login_url = 'login')
def ajax_messages_list(request):
    request.user.last_messages.all().update(is_acknowleged = True)
    
    messages_page = int(request.GET.get('messages_page'))
    last_messages_list = Paginator(request.user.last_messages.all().order_by("-message__id"), 20).get_page(messages_page)
    
    messages_list = []

    for message in last_messages_list:
        try:
            url = message.friend.profile.picture_150.url
        except:
            url = f"/static/images/letters/{ message.friend.first_name[0]}.jpg"
        messages_list.append(
            {
                'id' : message.id,
                'name' : message.friend.full_name(),
                'is_user_sender' : message.message.sender == request.user,
                'text' : message.message.text,
                'image_url' : url,
                'reciever_id' : message.friend.id,
                'is_seen' : message.is_seen,
            }
        )
    
    return HttpResponse(json.dumps([messages_list, last_messages_list.has_next(), last_messages_list.has_previous()]))

@login_required(login_url = 'login')
def messages_box(request, reciever_id):
    last_active(request)
    if reciever_id == request.user.id :
        return redirect('home')
        
    reciever = Account.objects.get(id=reciever_id)
    context={
        "reciever" : reciever,
        "title" : gettext('Messages'),
    }
    
    return render(request, 'message/messages_box.html', context)


@login_required(login_url = 'login')
def ajax_save_message(request, reciever_id):
    try:
        reciever = Account.objects.get(id = reciever_id)
    except:
        raise Http404

    if request.method == "POST":
        text = request.POST.get('message').strip()
        if text :
            message = Message.objects.create(
                reciever=reciever,
                sender = request.user,
                text = text,
            )        
            
    return HttpResponse()
    

def ajax_load_messages(request, reciever_id):
    
    try:
        last_message = request.user.last_messages.get(friend__id = int(reciever_id))
        last_message.is_seen = True
        last_message.save()
    except:
        pass
    page = int(request.GET.get('page'))
    paginator = Paginator(Message.objects.filter(
        Q(Q(sender = request.user, reciever__id = reciever_id) 
        | Q(reciever = request.user, sender__id = reciever_id))
    ).order_by("-id"), 40)
    show_prev = True
    show_next = True
    pages_count = paginator.num_pages
    if page <= 1 :
        page = 1
        show_next = False

    if page >= pages_count:
        page = pages_count
        show_prev = False
    
 
    messages = paginator.get_page(page)
    data = []
    messages_list = []
    for message in messages:
        messages_list.insert(0 ,{
            'text' : message.text,
            'is_user_sender' : message.sender == request.user,
            "id" : message.id,
            "time" : message.created_at.strftime('%d/%m/%Y %H:%M'),
        })
    data.append(messages_list)
    return HttpResponse(json.dumps([data, page, show_prev, show_next]))