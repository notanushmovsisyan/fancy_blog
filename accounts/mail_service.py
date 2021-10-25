from django.core import mail


def send_mail(token, uidb64, email):
    mail.send_mail(subject='Password Reset',
                   message=f'myfrontend.com/password-reset?token={token}&uidb64={uidb64}',
                   from_email='artak@mail.ru',
                   recipient_list=[email],
                   )
