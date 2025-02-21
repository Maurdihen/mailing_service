from django.apps import AppConfig

class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'

    def ready(self):
        # Запускаем планировщик только в основном процессе
        import os
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
            
        from . import scheduler
        scheduler.start() 