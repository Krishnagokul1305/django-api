from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_internship_registration_email(user_name, user_email, title, current_year):
    html_content = render_to_string('emails/registration.html', {
        'user_name': user_name,
        'title': title,
        'type': 'Internship',
        'email': user_email,
        'current_year': current_year,
    })

    # message = EmailMessage(
    #     subject="Registration received",
    #     body=html_content,
    #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
    #     to=[user_email],
    # )

    # message.content_subtype = "html"
    # message.send(fail_silently=False)

    return True


@shared_task
def send_internship_status_email(user_name, user_email, title, status, rejection_reason):
    html_content = render_to_string('emails/registrationStatus.html', {
        'user_name': user_name,
        'title': title,
        'type': 'Internship',
        'status': status,
        'rejection_reason': rejection_reason or '',
    })

    # message = EmailMessage(
    #     subject="Application status updated",
    #     body=html_content,
    #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
    #     to=[user_email],
    # )

    # message.content_subtype = "html"
    # message.send(fail_silently=False)

    return True
