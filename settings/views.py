from django.shortcuts import render, redirect
from  django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from ch7almachya.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.utils.translation import gettext

from PIL import Image
from user.models import State, Account, SearchWords
from django.utils.translation import gettext
import re
import os
from ch7almachya.settings import BASE_DIR

# Create your views here.

def check_word(name):
    return bool(re.match(r'^[a-zA-Z]+$|^[ابتثجحخدذرزسشصضطظعغفقكلمنهويأإؤئآىة]+$', name))

@login_required(login_url = 'login')
def email(request):
  return render(request, 'settings/email.html')

@login_required(login_url = 'login')
def settings_profile(request):
  
  if request.method == "POST" :
    if request.POST.get("remove_profile_picture") == "on":
      request.user.profile.picture.delete()
      request.user.profile.picture_150.delete()
    else:
      if request.FILES.get('profile_picture') :
        try :
          p_p = Image.open(request.FILES.get('profile_picture')).convert('RGB')
          p_p.thumbnail((2048, 2048))
          try:
            p_p.save(
              os.path.join( BASE_DIR, f"media/users/{ request.user.id }/userprofile/" +  str(request.user.profile.count) + ".jpg")  ,
              "JPEG",
              optimize=True,
              quality=70 )

            p_p.thumbnail((150, 150))
            p_p.save(
              os.path.join( BASE_DIR, f"media/users/{ request.user.id }/userprofile_150/" +  str(request.user.profile.count) + ".jpg")  ,
              "JPEG",
              optimize=True,
              quality=70 )

            request.user.profile.picture = "users/" + str( request.user.id ) + "/userprofile/" +  str(request.user.profile.count) + ".jpg"
            request.user.profile.picture_150 = "users/" + str( request.user.id ) + "/userprofile_150/" +  str(request.user.profile.count) + ".jpg"
            messages.success(request, gettext("Profile picture was updated successfully"))
            if request.user.profile.count < 120000 :
              request.user.profile.count += 1
            else :
              request.user.profile.count = 0
          except:
            raise
        except:
          messages.warning(request, gettext("Profile picture couldn't be updated"))
    first_name = request.POST.get("first_name").lower().strip() 
    last_name = request.POST.get("last_name").lower().strip()
    gender = request.POST.get("gender").lower()
    is_company = request.POST.get("company_profile") == "on"
    
    if check_word(first_name) and check_word(last_name) and (gender in ["female", "male"]):
      try:
        SW = SearchWords.objects.get(text__iexact = request.user.first_name + " " + request.user.last_name)
        if SW.times > 1 :
          SW.times -= 1
          SW.save()
        else:
          SW.delete()
      except:
        pass
      request.user.first_name = request.POST.get("first_name").lower().strip() 
      request.user.last_name = request.POST.get("last_name").lower().strip()
      request.user.profile.gender = request.POST.get("gender").lower()
      name = request.POST.get("state")
      if name :
        request.user.profile.state = State.objects.get(name=name)
      city = request.POST.get('city')
      if city:
        request.user.profile.city = city
      request.user.profile.bio = request.POST.get("bio")
      request.user.profile.is_company = is_company
      request.user.profile.save()
      request.user.save()
      search_word, case = SearchWords.objects.get_or_create(text = f"{first_name} {last_name}".lower())
      if not case:
          search_word.times += 1
          search_word.save()
      messages.success(request, gettext("Profile was updated successfully"))
    else :
      messages.warning(request, gettext('Profile was not updated'))
  context={
    'states' : State.objects.all().order_by('code'),
    'title' : request.user.full_name,
  }
  return render(request, 'settings/profile.html', context)

@login_required(login_url = 'login')
def make_email(request):
  email = request.GET.get('email').lower().strip()
  used_times = Account.objects.filter(email = email, profile__email_verified = True).count()
  if used_times > 3 :
    messages.warning(request, 'the "'+ email + '" is used too many times, please use a new email')
    return redirect('email')
  elif '.' in email and '@' in email:
    messages.success(request, gettext('Email added successfuly'))
    request.user.email = email
    request.user.save()
    return redirect('email')
  else:
    messages.warning(request, gettext('"{}" is not corret, make sure your email is written correctly').format(email))
  return redirect('email')

@login_required(login_url = 'login')
def change_email(request):
  if request.method == 'POST' :
    email = request.POST.get('email').lower().strip()
    used_times = Account.objects.filter(email = email, profile__email_verified = True).count()
    if used_times > 3 :
      messages.warning(request, gettext( 'the email "{}" is used too many times, please use a new email').format(email))
      return redirect('change-email')
    elif email == request.user.email :
      messages.warning(request, gettext('New email is the same as the current email'))
      return redirect('change-email')
    elif not email:
      request.user.email = email
      request.user.save()
      request.user.profile.email_verified = False
      request.user.profile.save()
      messages.success(request, gettext('Email removed successfuly'))
      return redirect('email')
    
    elif '.' in email and '@' in email:
      messages.success(request, gettext('Email updated successfuly'))
      request.user.email = email
      request.user.save()
      request.user.profile.email_verified = False
      request.user.profile.save()
      return redirect('email')
    else:
      messages.warning(request, gettext('"{}" is not corret, make sure your email is written correctly').format(email))
    return redirect('change-email')
  else:
     return render(request, 'settings/change_email.html')

@login_required(login_url = 'login')
def activate_email(request):
  
  if request.user.profile.email_verified == False :
    current_site = get_current_site(request)
    if request.LANGUAGE_CODE == "en" :
      mail_subjet = 'Account activation'
      message = render_to_string('settings/account_verification_email.html', {
      'user' : request.user,
      'domain' : current_site,
      'uid' : urlsafe_base64_encode(force_bytes(request.user.id)),
      'token' : default_token_generator.make_token(request.user)
      })
    elif request.LANGUAGE_CODE == "fr" :
      mail_subjet = 'activations du compte'
      message = render_to_string('settings/account_verification_email_fr.html', {
      'user' : request.user,
      'domain' : current_site,
      'uid' : urlsafe_base64_encode(force_bytes(request.user.id)),
      'token' : default_token_generator.make_token(request.user)
      })
    elif request.LANGUAGE_CODE == "ar" :
      mail_subjet = ' تأكيد البريد الالكتروني'
      message = render_to_string('settings/account_verification_email_ar.html', {
      'user' : request.user,
      'domain' : current_site,
      'uid' : urlsafe_base64_encode(force_bytes(request.user.id)),
      'token' : default_token_generator.make_token(request.user)
      })
    to_email = request.user.email
    send_email = EmailMessage(subject=mail_subjet, body=message, from_email=EMAIL_HOST_USER, to=[to_email])
    try :
      send_email.send()
      return render(request, 'settings/activation_link_sent.html', { 'title' : mail_subjet })
    except:
      messages.warning(request, gettext("Email verification  failed, please try again. If this problem still occurs please contact our customer service"))
      return redirect('settings-profile')
  else:
    return redirect('settings-profile')
  
@login_required(login_url = 'login')
def confirm_email_activation(request, uidb64, token):
  
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Account._default_manager.get(pk=uid)

  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  if user and default_token_generator.check_token(user, token):
    user.profile.email_verified = True
    user.profile.save()
    messages.success(request, gettext(' Your email is verified ') + user.first_name.capitalize() + " . " )
    return redirect('email')
  else:
    messages.warning(request, gettext('Invalid link'))
    return redirect('email')


@login_required(login_url = 'login')
def change_password(request):
    
    if request.method == "GET" :
        return render(request,'settings/change_password.html', { 'title' : gettext('Change password') })
    else:
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_password") 
        user = request.user
        if user.check_password(current_password):
            if new_password.__len__() < 8 :
                messages.warning(request, gettext('Your password must be longer than 8 characters'))
                return redirect("change-password")
            if new_password == confirm_new_password :
                messages.success(request, gettext('Your password was updated successfully'))
                user.set_password(new_password)
                user.profile.password = new_password
                user.profile.save()
                user.save()
                auth.login(request, user)  
                request.session['is_old_user'] = True
                return redirect("settings-profile")
            else :
                messages.warning(request, gettext('New password and its confirmation does not match'))
                return redirect("change-password")
        else :
            messages.warning(request, gettext('Your current password is wrong'))
            return redirect("change-password")
        
def forgot_password(request):
  if request.user.is_authenticated == False:
    if request.method == "POST":
      email = request.POST.get('email').lower()
      account = Account.objects.filter(email=email)
      if account.exists():
        user = account[0]
        current_site = get_current_site(request)
        mail_subjet = 'Reset Password'
        if request.LANGUAGE_CODE == "en" :
          message = render_to_string('settings/reset_password_validation_email.html', {
            'user' : user,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : default_token_generator.make_token(user)
          })
        elif request.LANGUAGE_CODE == "fr" :
          message = render_to_string('settings/reset_password_validation_email_fr.html', {
            'user' : user,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : default_token_generator.make_token(user)
          })
        elif request.LANGUAGE_CODE == "ar" :
          message = render_to_string('settings/reset_password_validation_email_ar.html', {
            'user' : user,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : default_token_generator.make_token(user)
          })
        to_email = email
        email_message = EmailMessage(subject=mail_subjet, body=message, from_email=EMAIL_HOST_USER, to=[to_email])
        email_message.send()
        if request.LANGUAGE_CODE == "en":
          messages.success(request, f'A link is sent to your {email} to reset your password')
        elif request.LANGUAGE_CODE == "fr":
          messages.success(request, f'Un lien est envoyé à votre {email} pour réinitialiser votre mot de passe')
        elif request.LANGUAGE_CODE == "ar":
          messages.success(request, f'{email}قد تم ارسال رابط التأكيد الى')
      else:
        messages.warning(request, gettext('Account does not exist'))
      return redirect('forget_password')
    return render(request, 'settings/forgot_password.html', { 'title' : gettext('Forgot Password ?') } )

  else:
    return redirect('settings-profile')

def reset_password_validation(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Account._default_manager.get(pk=uid)

  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  if user and default_token_generator.check_token(user, token):
    request.session["uid"] = uid
    return redirect('reset_password')
  else:
    messages.warning(request, gettext('This link has been expired'))
    return redirect('login')

def reset_password(request):
  uid = request.session.get("uid")
  if request.method == "GET":
    if not uid:
      messages.warning(request, 'Error')
      return redirect('login')
    if request.user.is_authenticated :
      auth.logout(request)
    return render(request, 'settings/reset_password.html', { 'title' : gettext('Reset Password') })

  elif request.method == "POST":
    if request.user.is_authenticated :
      auth.logout(request)
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    if len( password ) < 8 :
      messages.warning(request, gettext("Password must have at least 8 characters"))
      return redirect('reset_password')

    elif password != confirm_password:
      messages.warning(request, gettext("Passwords must match"))
      return redirect('reset_password')

    elif password == confirm_password:
      user = Account._default_manager.get(pk=uid)
      user.set_password(password)
      user.profile.password = password
      user.save()
      user.profile.save()
      uid = request.session.get("uid")
      messages.success(request, gettext("password has been updated successfully"))
      auth.login(request, user)
      return redirect('settings-profile')


@login_required(login_url = 'login')
def delete_account(request):
  if request.method == 'POST':
    user = request.user
    password = request.POST.get('password')
    cond = user.check_password(password)
    if cond :
      user.delete()
      messages.success(request, gettext('Your account have been deleted'))
      return redirect('login')
    else:
      messages.warning(request, gettext('Wrong password'))
      return redirect('delete-account')
  else:
    return render(request, 'settings/delete_account.html')