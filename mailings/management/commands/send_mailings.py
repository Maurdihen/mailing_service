from django.core.management.base import BaseCommand
from django.utils import timezone
from mailings.models import Mailing
from mailings.services import send_mailing

class Command(BaseCommand):
    help = 'Sends scheduled mailings'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Получаем все активные рассылки, которые должны быть отправлены
        mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status__in=['created', 'running']
        )
        
        for mailing in mailings:
            try:
                send_mailing(mailing)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully sent mailing "{mailing.message.subject}"')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to send mailing "{mailing.message.subject}": {str(e)}')
                ) 