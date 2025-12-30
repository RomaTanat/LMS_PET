from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("submit-solution/<int:problem_id>/", views.submit_solution, name="submit_solution"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("profile/edit/", views.EditProfileView.as_view(), name="edit_profile"),
    path("notification/<int:notification_id>/read/", views.mark_as_read, name="mark_as_read"),
    path("task/<int:task_id>/update/", views.update_task_status, name="update_task_status"),
    path("task/<int:task_id>/comment/", views.add_task_comment, name="add_task_comment"),
    path("about/", views.about, name="about"),

    # Gamification
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/buy/<int:item_id>/', views.buy_item_view, name='buy_item'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('clans/', views.ClanListView.as_view(), name='clan_list'),
    path('clans/create/', views.create_clan, name='create_clan'),
    path('clans/<int:clan_id>/join/', views.join_clan, name='join_clan'),
]
