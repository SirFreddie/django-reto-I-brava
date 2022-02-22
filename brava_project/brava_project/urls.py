"""brava_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from django.core import serializers

from polls.models import Question, User

from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/user/{int:user_id}")
def get_user(request, user_id: int):
    data = serializers.serialize('json', User.objects.filter(pk=user_id) )
    return data

@api.get("/users")
def get_users(request):
    data = serializers.serialize('json', User.objects.all())
    return data

@api.get("/emails")
def get_emails(request):
    aux = []
    all_users = User.objects.all()
    for user in all_users:
        if user.email != '':
            aux.append(user.email)
    return aux

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]