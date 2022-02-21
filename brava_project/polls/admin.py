from django.contrib import admin

from .models import Empresa, Question, User, Choice
from .logicaldelete import LogicalDeletedModelAdmin, LogicaLDeletedModelTabularInLine

class ChoiceInline(LogicaLDeletedModelTabularInLine):
    model = Choice
    extra = 3

class QuestionAdmin(LogicalDeletedModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    

admin.site.register(Question, QuestionAdmin)
admin.site.register(User)
admin.site.register(Choice)
admin.site.register(Empresa)