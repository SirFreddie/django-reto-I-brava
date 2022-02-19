from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from polls.models import User

from django.conf import settings


def send_mass_email():
    send_to = [] # Array con usuarios a enviar el correo.

    template = get_template('polls/correo.html')
    content = template.render()

    no_phone_users = User.objects.filter(phone_number='') # Devuelve una tabla con todos los usuarios sin telefono

    for user in no_phone_users:
        send_to.append(user.email)

    email = EmailMultiAlternatives(
        'Test email', # Asunto
        'Here is the message.', # Mensaje
        settings.EMAIL_HOST_USER, # Quien envia
        send_to, # Quienes reciben
    )

    email.attach_alternative(content, 'text/html') # Contenido creado con html
    email.send()
    print('SCHEDULED EMAILS SENT')