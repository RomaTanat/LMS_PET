from django.urls import path
from .views import CourseListView, CourseDetailView, UserProfileView, home, about, submit_solution

urlpatterns = [
    path("", home, name="home"),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("submit-solution/<int:problem_id>/", submit_solution, name="submit_solution"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("about/", about, name="about"),
]
