from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Client, Message, Mailing

class Command(BaseCommand):
    help = 'Creates manager group with necessary permissions'

    def handle(self, *args, **options):
        # Создаем группу менеджеров
        manager_group, created = Group.objects.get_or_create(name='Managers')
        
        if created:
            # Получаем все разрешения для наших моделей
            content_types = ContentType.objects.get_for_models(Client, Message, Mailing)
            
            permissions = []
            for content_type in content_types.values():
                permissions.extend(Permission.objects.filter(content_type=content_type))
            
            # Добавляем разрешения группе
            manager_group.permissions.add(*permissions)
            
            self.stdout.write(self.style.SUCCESS('Successfully created manager group'))
        else:
            self.stdout.write(self.style.WARNING('Manager group already exists')) 