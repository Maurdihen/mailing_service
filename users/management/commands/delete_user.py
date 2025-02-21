from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Удаляет пользователя по username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Пользователь {username} успешно удален'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Пользователь {username} не найден')) 