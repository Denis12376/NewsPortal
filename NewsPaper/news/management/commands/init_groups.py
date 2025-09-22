from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post


class Command(BaseCommand):
    help = 'Создание групп common и authors с соответствующими правами'

    def handle(self, *args, **options):
        # Создаем группу common
        common_group, created = Group.objects.get_or_create(name='common')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа common создана'))

        # Создаем группу authors и добавляем права
        authors_group, created = Group.objects.get_or_create(name='authors')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа authors создана'))

        # Получаем права для модели Post
        content_type = ContentType.objects.get_for_model(Post)
        post_permissions = Permission.objects.filter(content_type=content_type)

        # Добавляем права создания, изменения и удаления постов для authors
        for perm in post_permissions:
            authors_group.permissions.add(perm)

        self.stdout.write(
            self.style.SUCCESS('Группы common и authors успешно созданы с соответствующими правами')
        )