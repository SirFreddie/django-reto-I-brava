import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

from .logicaldelete import LogicalDeletedModel


class Question(LogicalDeletedModel):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(LogicalDeletedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Empresa(LogicalDeletedModel):
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class User(AbstractUser, LogicalDeletedModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True)
    phone_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username
