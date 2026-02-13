from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_verification_email(user_name, user_email, verification_token):
    frontend = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    verification_path = f"/verify-email/?token={verification_token}"
    verification_url = frontend.rstrip('/') + verification_path

    html_content = render_to_string('emails/emailverification.html', {
        'user_name': user_name,
        'verification_url': verification_url,
    })

    # message = EmailMessage(
    #     subject="Verify your email",
    #     body=html_content,
    #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
    #     to=[user_email],
    # )

    # message.content_subtype = "html"
    # message.send(fail_silently=False)

    return True


@shared_task
def send_welcome_email(user_name, user_email):
    html_content = render_to_string('emails/welcomeuser.html', {
        'user_name': user_name,
        'email': user_email,
    })

    # message = EmailMessage(
    #     subject="Welcome to Liture",
    #     body=html_content,
    #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
    #     to=[user_email],
    # )

    # message.content_subtype = "html"
    # message.send(fail_silently=False)

    return True


@shared_task
def send_password_reset_email(user_name, user_email, reset_link, dashboard_url):
    html_content = render_to_string('emails/resetpassword.html', {
        'user_name': user_name,
        'user_email': user_email,
        'reset_link': reset_link,
        'dashboard_url': dashboard_url,
    })

    # message = EmailMessage(
    #     subject="Password reset request",
    #     body=html_content,
    #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
    #     to=[user_email],
    # )

    # message.content_subtype = "html"
    # message.send(fail_silently=False)

    return True
