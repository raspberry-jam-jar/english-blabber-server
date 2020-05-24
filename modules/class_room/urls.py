from django.urls import path

from class_room import views


app_name = 'class_room'

urlpatterns = [
    path(r'apply/', views.SocialUserViewSet.as_view({'post': 'create'}),
         name='apply_to_join'),
    path(r'vk_auth/', views.VkSocialUserAuth.as_view(), name='vk_auth'),
]
