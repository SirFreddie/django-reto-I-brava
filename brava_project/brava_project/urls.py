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
from typing import List

from polls.models import Question, User, Choice

from ninja import NinjaAPI
from ninja import ModelSchema


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = "__all__"

class QuestionSchema(ModelSchema):
    class Config:
        model = Question
        model_fields = "__all__"

class ChoiceSchema(ModelSchema):
    class Config:
        model = Choice
        model_fields = "__all__"

api = NinjaAPI()

@api.get("/user/{int:user_id}", response=UserSchema)
def get_user(request, user_id: int):
    data = User.objects.filter(pk=user_id).first()
    return data

@api.get("/users", response=List[UserSchema])
def get_users(request):
    data = User.objects.all()
    return list(data)

@api.get("/questions", response=List[QuestionSchema])
def get_questions(request):
    data = Question.objects.all()
    return list(data)

@api.get("/choices", response=List[ChoiceSchema])
def get_choices(request):
    data = Choice.objects.all()
    return list(data)

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