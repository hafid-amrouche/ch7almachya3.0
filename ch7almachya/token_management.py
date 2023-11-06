from user.models import TokenSessionId
from django.http import HttpResponse
from user.models import TokenSessionId
from django.contrib.sessions.models import Session
import json

def logout_user_by_session_id(session_id):
    try:
        # Retrieve the session associated with the given session ID
        session = Session.objects.get(session_key=session_id)
        
        # Clear the session data to log the user out
        session.delete()
        
        # Optionally, you can perform additional actions (e.g., redirect the user)
        
        return True  # Indicate that the user has been successfully logged out
    except Session.DoesNotExist:
        # Handle the case where the session does not exist
        return False

def update_notifications_token_list(request):
    try :
        current_token = str(request.GET.get('token'))
        TokenSessionId.objects.get_or_create(user=request.user, token=current_token, session_id=request.COOKIES.get('sessionid'))
        tokens = TokenSessionId.objects.filter(user=request.user)
        
        if tokens.count() > 5 :
            to_be_deleted = tokens.order_by('-id')[5:]
            for token in to_be_deleted :
                logout_user_by_session_id(token.session_id)
                token.delete()
            

        tokens_list = list(tokens.values_list('token', flat=True))
        request.user.notifications_token.tokens_list = json.dumps(tokens_list)
        request.user.notifications_token.save()
    
        return HttpResponse(json.dumps([current_token]))
    except :
        print('ERROR AT ch7almachya.token_management.update_notifications_token_list')
        return HttpResponse(json.dumps('ERROR UPDATING R-TOKEN'))
    

def refresh_token(request):
    try :
        refresh_token = str(request.GET.get('token'))
        token_seesion_id = TokenSessionId.objects.get(user=request.user, session_id=request.COOKIES.get('sessionid'))
        token_seesion_id.token = refresh_token
        token_seesion_id.save()
        tokens = TokenSessionId.objects.filter(user=request.user)            

        tokens_list = list(tokens.values_list('token', flat=True))
        request.user.notifications_token.tokens_list = json.dumps(tokens_list)
        request.user.notifications_token.save()
    
        return HttpResponse(json.dumps([refresh_token]))
    except :
        print('ERROR AT ch7almachya.token_management.refresh_token')
        return HttpResponse(json.dumps('ERROR UPDATING R-TOKEN'))