from .models import Notification

def notification_context(request):
    if not request.user.is_authenticated:
        return {}
    return {
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count()
    }
