from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Lms_project import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("lms.urls")),  # Подключаем маршруты из приложения lms
    path("accounts/", include("accounts.urls")),  # Подключаем маршруты аутентификации
    path("chat/", include("chat.urls")),  # Подключаем маршруты чата
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
