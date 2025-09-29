from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail

from .models import Post, Category
from django.contrib.auth.models import User

@shared_task
def send_weekly_digest():
    week_ago = timezone.now() - timedelta(days=7)
    all_users = User.objects.filter(email__isnull=False).exclude(email='')
    new_posts = Post.objects.filter(
        created_at__gte=week_ago
    ).distinct().order_by('-created_at')
    for user in all_users:
        try:
            if user.email:
                send_user_weekly_digest(user, new_posts)

        except Exception as e:
            print(f"Ошибка при отправке рассылки пользователю {user.username}: {e}")

    return f"Рассылка отправлена!"



def send_user_weekly_digest(user, posts):
    posts_list = "Новые статьи за последнюю неделю:\n\n"
    for i, post in enumerate(posts, 1):
        posts_list += f"{i}. {post.title}\n"
        posts_list += f"   Категории: {', '.join([cat.name for cat in post.categories.all()])}\n"
        posts_list += f"   Дата: {post.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        posts_list += f"   Краткое содержание: {post.content[:100]}...\n"
        posts_list += f"   Ссылка: {settings.SITE_URL}/posts/{post.id}/\n\n"

    send_mail(
        subject='Еженедельная рассылка новостей',
        message=posts_list,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


@shared_task
def send_post_notifications_task(post_id):
    try:
        post = Post.objects.get(id=post_id)
        post_categories = post.categories.all()
        for category in post_categories:
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                if subscriber.email:
                    try:
                        send_post_notification.delay(
                            subscriber.id,
                            post.id,
                            category.id
                        )
                    except Exception as e:
                        print(f"Ошибка постановки задачи для {subscriber.username}: {e}")

    except Post.DoesNotExist:
        return f"Пост с ID {post_id} не найден"
    except Exception as e:
        return f"Ошибка при обработке поста {post_id}: {e}"


@shared_task
def send_post_notification(user_id, post_id, category_id):
    try:
        from django.contrib.auth.models import User
        from .models import Post, Category

        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        category = Category.objects.get(id=category_id)
        message = f'''Привет, {user.username}!
        На нашем портале новая публикация в категории "{category.name}"!
        Заголовок: {post.title}
        Краткое содержание: {post.content[:100]}...
        Автор: {post.author.user.username}
        Читать полностью: {settings.SITE_URL}/news/{post.id}/
        '''

        send_mail(
            subject=f'Новая публикация в категории "{category.name}"!',
            message=message.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        return f"Ошибка отправки уведомления: {e}"
