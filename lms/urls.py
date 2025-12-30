from django.urls import path
from .views import CourseListView, CourseDetailView, UserProfileView, home, about, submit_solution, update_task_status, add_task_comment, mark_as_read

urlpatterns = [
    path("", home, name="home"),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("submit-solution/<int:problem_id>/", submit_solution, name="submit_solution"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("notification/<int:notification_id>/read/", mark_as_read, name="mark_as_read"),
    path("task/<int:task_id>/update/", update_task_status, name="update_task_status"),
    path("task/<int:task_id>/comment/", add_task_comment, name="add_task_comment"),
    path("about/", about, name="about"),
]
