from django.core.mail import send_mail

send_mail(
    'ALERTA ATENCION SUCURSAL Santa Ana N12',
    'Here is the message.',
    'pabloovejero110@gmail.com',
    ['pabloovejero110@msn.com'],
    fail_silently=False
)
