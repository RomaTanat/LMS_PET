"""
Redis caching utilities for the LMS application.
"""
from django.core.cache import cache
from django.conf import settings
from functools import wraps
import json


class CacheKeys:
    """Cache key constants"""
    COURSE_LIST = 'courses:list'
    COURSE_DETAIL = 'course:{}:detail'
    USER_COURSES = 'user:{}:courses'
    USER_ACHIEVEMENTS = 'user:{}:achievements'
    
    @staticmethod
    def course_detail(course_id):
        return CacheKeys.COURSE_DETAIL.format(course_id)
    
    @staticmethod
    def user_courses(user_id):
        return CacheKeys.USER_COURSES.format(user_id)
    
    @staticmethod
    def user_achievements(user_id):
        return CacheKeys.USER_ACHIEVEMENTS.format(user_id)


def cache_course_list(timeout=300):
    """Cache decorator for course list"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_data = cache.get(CacheKeys.COURSE_LIST)
            if cached_data is not None:
                return cached_data
            
            result = func(*args, **kwargs)
            cache.set(CacheKeys.COURSE_LIST, result, timeout)
            return result
        return wrapper
    return decorator


def cache_course_detail(timeout=900):
    """Cache decorator for course detail"""
    def decorator(func):
        @wraps(func)
        def wrapper(course_id, *args, **kwargs):
            cache_key = CacheKeys.course_detail(course_id)
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data
            
            result = func(course_id, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


def invalidate_course_cache(course_id=None):
    """Invalidate course caches"""
    cache.delete(CacheKeys.COURSE_LIST)
    if course_id:
        cache.delete(CacheKeys.course_detail(course_id))


def invalidate_user_cache(user_id):
    """Invalidate user-related caches"""
    cache.delete(CacheKeys.user_courses(user_id))
    cache.delete(CacheKeys.user_achievements(user_id))


def get_or_set_cache(key, callable_func, timeout=300):
    """Generic cache get or set"""
    cached_data = cache.get(key)
    if cached_data is not None:
        return cached_data
    
    data = callable_func()
    cache.set(key, data, timeout)
    return data


def push_notification(user_id, notification_data):
    """Push real-time notification to Redis for user"""
    notification_key = f'notifications:user:{user_id}'
    
    # Get existing notifications
    notifications = cache.get(notification_key, [])
    
    # Add new notification
    notifications.append({
        **notification_data,
        'timestamp': str(notification_data.get('timestamp', ''))
    })
    
    # Keep only last 50 notifications
    notifications = notifications[-50:]
    
    # Store back in cache
    cache.set(notification_key, notifications, timeout=86400)  # 24 hours
    
    return notifications


def get_user_notifications(user_id):
    """Get user notifications from Redis"""
    notification_key = f'notifications:user:{user_id}'
    return cache.get(notification_key, [])


def clear_user_notifications(user_id):
    """Clear user notifications"""
    notification_key = f'notifications:user:{user_id}'
    cache.delete(notification_key)
