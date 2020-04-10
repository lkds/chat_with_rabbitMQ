from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
import chat.rabbitMQ

# Create your views here.
def login(request):
    if (request.method == 'GET'):
        return render(request,'chat.html')