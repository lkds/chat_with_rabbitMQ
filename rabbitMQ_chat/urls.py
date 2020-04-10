"""rabbitMQ_chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import chat.views as chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/login/', chat_view.login),
    path('chat/sendMsg/<str:sendUser>/<str:targetUser>/<str:msgType>/<str:msg>/', chat_view.sendMsg),#sendUser, targetUser, msgType, msg
    path('chat/getMsg/<str:id>/',chat_view.getMsg),   
]
