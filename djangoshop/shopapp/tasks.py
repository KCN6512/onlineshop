from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_mail():
    send_mail('Subject here',
    'Here is the message.',
    'djangoshop@app.com',
    ['user@email'],
    fail_silently=False,)

@shared_task
def test_task(word, word2):
    print('1 minute has passed')
    print(f'{word} {word2}')