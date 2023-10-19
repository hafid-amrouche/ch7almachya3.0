
from datetime import datetime as dt, timezone
from funtions import get_ip_address

def user(request):
  ip_address = get_ip_address(request)
  is_old_user = request.session.get('is_old_user')
  request.session["is_old_user"] = True
  
  context = {
    "is_old_user" : is_old_user,
    "dt" : dt.now(timezone.utc),
    "ip_address" : ip_address,
    'dark_mode' : request.session.get('dark_mode')
  }
        
  

  return context