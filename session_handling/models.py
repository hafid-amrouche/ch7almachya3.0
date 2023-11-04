from django.contrib.sessions.middleware import SessionMiddleware
from user.models import TokenSessionId
import json

# class CustomSessionMiddleware(SessionMiddleware):
#     def process_response(self, request, response):
#         try :
#             print('Try')
#             # Check if the session has been deleted (e.g., due to expiration)
#             if request.session.get_expire_at_browser_close() or request.session.get('_session_expired'):
#                 print('igiug')
#                 # Execute your function or take necessary action here
#                 # For example, log the event, notify the user, or perform any other desired task
#                 # session_id = request.session.session_key
#                 # token_session_id = TokenSessionId.objects.get(session_id=session_id)
#                 # user = token_session_id.user
#                 # token_session_id.delete()
                
#                 # tokens = TokenSessionId.objects.filter(user=user)
#                 # tokens_list = list(tokens.values_list('token', flat=True))
#                 # user.notifications_token.tokens_list = json.dumps(tokens_list)
#                 # user.notifications_token.save()
               
    
                
#         except:
#             pass

#         return super().process_response(request, response)

from django.contrib.sessions.middleware import SessionMiddleware

class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
            # Check if the session ID is not stored as a custom session variable
            if '_custom_session_id' not in request.session:
                # Store the session ID as a custom session variable
                print(request.session.get('_custom_session_id'), request.session.session_key)
                request.session['_custom_session_id'] = request.session.session_key
                print(request.session.get('_custom_session_id'), request.session.session_key)

            elif request.session.get('_custom_session_id') != request.session.session_key:

                try:
                    session_id = request.session.get('_custom_session_id')
                    token_session_id = TokenSessionId.objects.get(session_id=session_id)
                    user = token_session_id.user
                    token_session_id.delete()
                    
                    tokens = TokenSessionId.objects.filter(user=user)
                    tokens_list = list(tokens.values_list('token', flat=True))
                    user.notifications_token.tokens_list = json.dumps(tokens_list)
                    user.notifications_token.save()
                    
                except:
                    pass

            return super().process_request(request)