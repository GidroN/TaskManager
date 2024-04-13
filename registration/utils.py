from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator


def send_email_for_verify(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    current_site = get_current_site(request)
    context = {
        'site_name': current_site.name,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
        'user': user,
    }

    message = render_to_string('registration/email_verify_message.html', context=context)
    email = EmailMessage('Подтвердите почту!', message, to=[user.email])
    print(email.body)
    email.send()
