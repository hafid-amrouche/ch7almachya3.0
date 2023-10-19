from django.shortcuts import redirect, render
from .models import Message
from user.models import Account, LastMessage
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from funtions import last_active
from django.utils.translation import gettext
from django.http import Http404, HttpResponse
import json
from ch7almachya.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

# Create your views here.
 
@login_required(login_url = 'login')
def messages_list(request):
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
    
    if reciever_id == request.user.id :
        return redirect('home')
    try :
        reciever = Account.objects.get(id=reciever_id)
    except:
        return render(request, 'error.html')
        

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
            
            # if reciever.profile.email_messages and reciever.profile.email_verified:
            #     try :
            #         url = 'http://' + str(get_current_site(request)) + f'/messages/{ request.user.id } :'
            #         mail_subjet = gettext('{} Sent a message').format(request.user.full_name())
            #         message = render_to_string('message/message_email.html', {
            #             'line_1' : gettext("Go to message {}:").format(url),
            #             'line_2' : gettext("{} said").format(request.user.first_name.capitalize()),
            #             'text' : text
            #         })
            #         to_email = reciever.email
            #         send_email = EmailMessage(subject=mail_subjet, body=message, from_email=EMAIL_HOST_USER, to=[to_email])
            #         send_email.send()
            #     except:
            #         pass
            user_last_message = request.user.last_messages.filter(friend = reciever)
            reciever_last_message = reciever.last_messages.filter(friend = request.user)
            if user_last_message:
                user_last_message = user_last_message[0]
                user_last_message.message = message
                user_last_message.is_seen = True
                user_last_message.save()
                reciever_last_message = reciever_last_message[0]
                reciever_last_message.message = message
                reciever_last_message.is_seen = False
                reciever_last_message.is_acknowleged = False
                reciever_last_message.is_acknowleged_by_browser = False
                reciever_last_message.is_acknowleged_by_android = False
                reciever_last_message.save()
            else:
                l1= LastMessage.objects.create(
                    user = request.user,
                    message = message,
                    friend = reciever,
                    is_seen = True,
                )
                l2 = LastMessage.objects.create(
                    friend = request.user,
                    message = message,
                    user = reciever,
                )
                
            request.user.friendlist.add_friend(reciever)
            reciever.friendlist.add_friend(request.user)
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