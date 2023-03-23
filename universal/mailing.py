from threading import Thread
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from queue import *

mail_from = settings.EMAIL_HOST_USER


concurrent = 50
que = Queue(concurrent*10)


def resetPassMail(subject, recipient_list, name, otp):
	html_content = render_to_string('mail/forgot_password_mail.html', {'name':name, 'otp':otp})
	text_content = strip_tags(html_content) 

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, mail_from, recipient_list)
	msg.attach_alternative(html_content, "text/html")
	msg.send()