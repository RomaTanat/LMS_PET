from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PersonalTask, Submission, Notification

@receiver(post_save, sender=PersonalTask)
def notify_task_assigned(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.student,
            title="Новая персональная задача",
            message=f"Вам назначена задача: {instance.title}",
            link=f"/profile/" # Перенаправляем на профиль (Канбан доску)
        )

@receiver(post_save, sender=Submission)
def notify_submission_checked(sender, instance, created, **kwargs):
    # Реагируем только на обновление (не создание) и если статус не PENDING
    if not created and instance.status != 'PENDING':
        Notification.objects.create(
            recipient=instance.student,
            title="Результат проверки кода",
            message=f"Задача '{instance.problem.title}' проверена. Статус: {instance.get_status_display()}",
            link=f"/courses/{instance.problem.material.section.course.id}/"
        )
