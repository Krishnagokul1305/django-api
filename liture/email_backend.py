# myapp/email_backend.py

from django.core.mail.backends.smtp import EmailBackend

class TimeoutEmailBackend(EmailBackend):
    def get_connection(self, fail_silently=False):
        connection = super().get_connection(fail_silently)
        connection.timeout = 60  # Timeout in seconds (set your preferred timeout)
        return connection
