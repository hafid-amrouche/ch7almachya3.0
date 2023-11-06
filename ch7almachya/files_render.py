from django.http import FileResponse, HttpResponse
from django.shortcuts import render
import os
from ch7almachya.settings import BASE_DIR

def firebase_messaging_sw(request):
    # Path to the file
    file_path = os.path.join(BASE_DIR, 'static/firebase-messaging-sw.js')   # Replace with the actual file path
    # Open the file and create a FileResponse
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        return response
    else:
        return HttpResponse('FILE NOT FOUND')
