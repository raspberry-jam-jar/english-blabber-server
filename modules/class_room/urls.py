from django.urls import path

from class_room import views


app_name = 'class_room'

urlpatterns = [
    path(
        r'status/<str:code>/', views.SocialUserStatusView.as_view(),
        name='social_user_status'
    ),
    path(r'apply/', views.SocialUserViewSet.as_view({'post':'create'}), name='apply_to_join')
]
