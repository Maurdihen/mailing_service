from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from django_apscheduler.jobstores import DjangoJobStore

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Запускаем проверку рассылок каждую минуту
    scheduler.add_job(
        call_command,
        'interval',
        minutes=1,
        args=('send_mailings',),
        id='send_mailings',
        replace_existing=True
    )
    
    scheduler.start() 