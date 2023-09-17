from .models import Notification
from Users.models import LoginDetail

def notification_count(request):
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
        
        login_activity_count = LoginDetail.objects.filter(user = request.user, is_read=False).count()
        
        return {
            'notification_count': notification_count,
            'login_activity_count':login_activity_count
            }
    return {}
