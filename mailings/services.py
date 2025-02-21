import logging
from django.core.mail import send_mail
from django.conf import settings
from .models import MailingAttempt

logger = logging.getLogger('mailings')

def send_mailing(mailing):
    """
    Отправляет рассылку всем получателям
    """
    logger.info(f'Starting mailing: {mailing.id} - {mailing.message.subject}')
    
    for client in mailing.clients.all():
        try:
            logger.info(f'Sending email to {client.email}')
            
            # Отправляем письмо
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER or 'test@example.com',
                recipient_list=[client.email],
                fail_silently=False,
            )
            
            # Создаем запись об успешной попытке
            MailingAttempt.objects.create(
                mailing=mailing,
                status='success',
                server_response='Email sent successfully'
            )
            
            logger.info(f'Successfully sent email to {client.email}')
            
        except Exception as e:
            error_message = str(e)
            logger.error(f'Failed to send email to {client.email}: {error_message}')
            
            # Создаем запись о неудачной попытке
            MailingAttempt.objects.create(
                mailing=mailing,
                status='failed',
                server_response=error_message
            )
    
    mailing.status = 'completed'
    mailing.save()
    logger.info(f'Completed mailing: {mailing.id}') 