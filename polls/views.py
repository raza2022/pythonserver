from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import time
import datetime

count = 1
@csrf_exempt
def index(request):
    # request.send_header('Access-Control-Allow-Origin', '*')
    # get the image by name can be changed
    base64_image_str = request.POST['croppedImage']

    # change base64 to image string else that line do nothing
    base64_image_str = base64_image_str[base64_image_str.find(",") + 1:]

    # decode string
    imageData = base64.b64decode(base64_image_str)

    # give unique file name and save in DB
    dt = time.time()
    filename = str(dt) + '.jpg'
    print (filename)
    with open(filename, 'wb') as f:
        f.write(imageData)

    #     return response
    return HttpResponse("Hello, world. You're at the polls index.")