from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save
from .tasks import send_post_notifications_task


from .models import Category, Post


@receiver(m2m_changed, sender=Category.subscribers.through)
def subscribers_notification(sender, instance, action, pk_set,**kwargs):
    if action == 'post_add':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Новая подписка',
            message=f'Привет, {user.username}! Вы подписались на категорию {instance.name}. Список категорий ваших подписок: {", ".join([cat.name for cat in user.categories.all()])}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    if action == 'post_remove':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Отписка от категории',
            message=f'Привет, {user.username}! Вы отписались от категорию {instance.name}. Список категорий ваших подписок: {", ".join([cat.name for cat in user.categories.all()])}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )


@receiver(m2m_changed, sender=Post.categories.through)
def post_categories_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        categories = instance.categories.filter(pk__in=pk_set)

        for category in categories:
            subscribers = category.subscribers.all()

            for user in subscribers:
                if user.email:
                    send_post_notification(user, instance, category)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if timezone.now().weekday() == 6:
            week_ago = timezone.now() - timedelta(days=7)
            subscribers = User.objects.filter(
                subscribed_categories__isnull=False
            ).distinct()

            for user in subscribers:
                if user.email:
                    user_categories = user.category.subscribers.all().all()
                    new_posts = Post.objects.filter(
                        categories__in=user_categories,
                        created_at__gte=week_ago
                    ).distinct().order_by('-created_at')
                    if new_posts.exists():
                        self.send_weekly_digest(user, user_categories, new_posts)

    def send_weekly_digest(self, user, categories, posts):
        posts_list = ""
        for i, post in enumerate(posts, 1):
            posts_list += f"{i}. {post.title} - {settings.SITE_URL}/posts/{post.id}/\n"
            posts_list += f"   Категории: {', '.join([cat.name for cat in post.categories.all()])}\n"
            posts_list += f"   Дата: {post.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            posts_list += f"   Кратко: {post.content[:20]}...\n\n"
        send_mail(
            subject='Еженедельная рассылка',
            message= posts_list,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
'''
def send_post_notification(user, post, category):
    send_mail(
        subject='Новая публикация!',
        message=f'Привет, {user.username}! На нашем новая публикация категории {category.name}\n'
                f'Краткое содержание: {post.content[:20]}\n'
                f'Автор: {post.author.user.username}\n'
                f'Читать полностью на Новостном портале! {settings.SITE_URL}/news/{post.id}/',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
 '''
@receiver(post_save, sender=Post)
def send_post_notification(sender, instance, created, **kwargs):
    if created:
        send_post_notifications_task.delay(instance.id)