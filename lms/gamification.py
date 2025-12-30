from datetime import datetime
from django.utils import timezone
from .models import Achievement, UserAchievement, ShopItem, UserInventory, Submission

def check_achievement(user, criteria_type, value=None):
    """
    Проверяет и выдает достижения пользователю.
    """
    achievements = Achievement.objects.filter(criteria_type=criteria_type)
    for achievement in achievements:
        user_achievement, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
        if created or user_achievement.progress < 100:
            if criteria_type == 'sniper' and value:
                # Value здесь - это успешно ли решение с первой попытки (Boolean)
                if value:
                    user_achievement.progress = 100
                    user_achievement.earned_at = timezone.now()
                    user_achievement.save()
                    # Можно отправить уведомление
            elif criteria_type == 'night_owl':
                # Проверка времени
                current_hour = timezone.localtime(timezone.now()).hour
                if 2 <= current_hour <= 5:
                    user_achievement.progress = 100
                    user_achievement.earned_at = timezone.now()
                    user_achievement.save()
            # Добавить другие проверки при необходимости

def process_submission_rewards(submission):
    """
    Начисляет награды за успешное решение задачи.
    """
    if submission.status != 'ACCEPTED':
        return

    user = submission.student
    profile = user.student_profile

    # 1. Начисление монет и XP
    # Базовые значения, можно усложнить в зависимости от сложности задачи
    xp_reward = 50
    coins_reward = 10

    profile.add_xp(xp_reward)
    profile.coins += coins_reward
    profile.save()

    # 2. Проверка ачивок

    # "Снайпер": Проверяем, есть ли другие попытки для этой задачи
    previous_attempts = Submission.objects.filter(
        student=user,
        problem=submission.problem
    ).exclude(id=submission.id).count()

    if previous_attempts == 0:
        check_achievement(user, 'sniper', value=True)

    # "Ночная сова"
    check_achievement(user, 'night_owl')

    # "Марафонец" - обрабатывается в update_streak модели, но можно проверить здесь ачивку
    if profile.streak_days >= 30:
         # check_achievement(user, 'marathon') # Предполагая, что такая логика есть
         pass

def purchase_item(user, item_id):
    """
    Покупка предмета в магазине.
    Возвращает (success, message).
    """
    try:
        item = ShopItem.objects.get(id=item_id)
        profile = user.student_profile

        if UserInventory.objects.filter(student=profile, item=item).exists():
            return False, "Предмет уже куплен."

        if profile.coins >= item.cost:
            profile.coins -= item.cost
            profile.save()
            UserInventory.objects.create(student=profile, item=item)
            return True, f"Вы купили {item.name}!"
        else:
            return False, "Недостаточно монет."
    except ShopItem.DoesNotExist:
        return False, "Предмет не найден."
    except Exception as e:
        return False, str(e)
