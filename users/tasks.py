from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_contact_email(name, email, phone, message):
	html_content = render_to_string('emails/contact.html', {
		'name': name,
		'email': email,
		'phone': phone,
		'message': message,
	})

	to_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
	message_obj = EmailMessage(
		subject=f"New contact message from {name}",
		body=html_content,
		from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
		to=[to_email] if to_email else [],
		reply_to=[email],
	)

	message_obj.content_subtype = "html"
	message_obj.send(fail_silently=False)

	return True
