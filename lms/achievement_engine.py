"""
Achievement engine for processing user activities and awarding achievements.
"""
from lms.models import Achievement, UserAchievement, User
from lms.cache import push_notification
import logging

logger = logging.getLogger(__name__)


class AchievementEngine:
    """Process events and award achievements"""
    
    @staticmethod
    def check_and_award_achievements(user_id, event_type, event_data):
        """Check if user earned any achievements based on event"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error(f"User {user_id} not found")
            return
        
        # Check different achievement types based on event
        if event_type == 'course_enrolled':
            AchievementEngine._check_course_count_achievements(user)
        
        elif event_type == 'course_completed':
            AchievementEngine._check_course_completion_achievements(user)
        
        elif event_type == 'test_passed':
            AchievementEngine._check_test_score_achievements(user, event_data.get('score', 0))
        
        elif event_type == 'user_login':
            AchievementEngine._check_login_streak_achievements(user)
    
    @staticmethod
    def _check_course_count_achievements(user):
        """Check achievements based on number of enrolled courses"""
        course_count = user.enrolled_courses.count()
        
        # Get all course_count achievements
        achievements = Achievement.objects.filter(criteria_type='course_count')
        
        for achievement in achievements:
            if course_count >= achievement.criteria_value:
                # Check if user already has this achievement
                user_achievement, created = UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement,
                    defaults={'progress': 100}
                )
                
                if created:
                    logger.info(f"User {user.username} earned achievement: {achievement.name}")
                    # Send notification
                    push_notification(user.id, {
                        'type': 'achievement_earned',
                        'achievement_name': achievement.name,
                        'achievement_icon': achievement.icon,
                        'points': achievement.points,
                        'message': f'Поздравляем! Вы получили достижение: {achievement.name}'
                    })
                else:
                    # Update progress
                    progress = min(100, int((course_count / achievement.criteria_value) * 100))
                    if user_achievement.progress < progress:
                        user_achievement.progress = progress
                        user_achievement.save()
    
    @staticmethod
    def _check_course_completion_achievements(user):
        """Check achievements for completing courses"""
        # This would need a completed_courses field or tracking
        # For now, similar to course_count
        AchievementEngine._check_course_count_achievements(user)
    
    @staticmethod
    def _check_test_score_achievements(user, score):
        """Check achievements based on test scores"""
        if score >= 100:
            # Perfect score achievement
            try:
                achievement = Achievement.objects.get(
                    criteria_type='test_score',
                    criteria_value=100
                )
                user_achievement, created = UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement,
                    defaults={'progress': 100}
                )
                
                if created:
                    logger.info(f"User {user.username} earned perfect score achievement")
                    push_notification(user.id, {
                        'type': 'achievement_earned',
                        'achievement_name': achievement.name,
                        'achievement_icon': achievement.icon,
                        'points': achievement.points,
                        'message': f'Идеальный результат! Вы получили: {achievement.name}'
                    })
            except Achievement.DoesNotExist:
                pass
    
    @staticmethod
    def _check_login_streak_achievements(user):
        """Check achievements for login streaks"""
        # This would require tracking login dates
        # Placeholder for future implementation
        pass
    
    @staticmethod
    def get_user_total_points(user):
        """Calculate total points for user"""
        user_achievements = UserAchievement.objects.filter(
            user=user,
            progress=100
        ).select_related('achievement')
        
        total_points = sum(ua.achievement.points for ua in user_achievements)
        return total_points
    
    @staticmethod
    def get_user_achievements_summary(user):
        """Get summary of user's achievements"""
        earned = UserAchievement.objects.filter(
            user=user,
            progress=100
        ).select_related('achievement')
        
        in_progress = UserAchievement.objects.filter(
            user=user,
            progress__lt=100,
            progress__gt=0
        ).select_related('achievement')
        
        return {
            'earned': list(earned),
            'in_progress': list(in_progress),
            'total_points': AchievementEngine.get_user_total_points(user),
            'earned_count': earned.count(),
        }
