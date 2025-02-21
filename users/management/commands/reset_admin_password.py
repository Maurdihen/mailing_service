from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Сбрасывает пароль администратора'

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(is_superuser=True)
            new_password = 'admin123'  # Новый пароль
            admin.set_password(new_password)
            admin.save()
            self.stdout.write(
                self.style.SUCCESS(f'Пароль администратора сброшен. Новый пароль: {new_password}')
            )
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Администратор не найден')) 