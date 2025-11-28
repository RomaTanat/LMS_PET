from django.urls import path
from .views import CourseListView, CourseDetailView, UserProfileView, home, about

urlpatterns = [
    path("", home, name="home"),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("about/", about, name="about"),
]
