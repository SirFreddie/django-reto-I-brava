from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from .models import Choice, Question, User

from django.conf import settings

def send_email(mail):
    context = {'mail': mail}

    template = get_template('polls/correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Test email', # Asunto
        'Here is the message.', # Mensaje
        settings.EMAIL_HOST_USER, # Quien envia
        [mail], # Quienes reciben
    )

    email.attach_alternative(content, 'text/html') # Contenido creado con html
    email.send()

def send_mass_email():
    send_to = [] # Array con usuarios a enviar el correo.

    template = get_template('polls/correo.html')
    content = template.render()

    no_phone_users = User.objects.filter(phone_number='') # Devuelve una tabla con todos los usuarios si telefono
    for user in no_phone_users:
        send_to.append(user.email)

    print(send_to)
    email = EmailMultiAlternatives(
        'Test email', # Asunto
        'Here is the message.', # Mensaje
        settings.EMAIL_HOST_USER, # Quien envia
        send_to, # Quienes reciben
    )

    email.attach_alternative(content, 'text/html') # Contenido creado con html
    email.send()

def email_view(request):

    if request.method == 'POST':
        single_mail = request.POST.get('mail')
        mass_email = request.POST.get('mass')
        if (single_mail):
            send_email(single_mail)    
            return HttpResponseRedirect('/../polls/')
        elif (mass_email):
            send_mass_email()
            return HttpResponseRedirect('/../polls/')

    return render(request, 'polls/email.html', {})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))