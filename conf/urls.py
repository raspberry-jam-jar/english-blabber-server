"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import pathlib

import django
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

import class_room.urls


def graphiql(request):
    """Trivial view to serve the `graphiql.html` file."""
    del request
    graphiql_filepath = pathlib.Path(__file__).absolute().parent / "graphiql.html"
    with open(graphiql_filepath) as f:
        return django.http.response.HttpResponse(f.read())


urlpatterns = [
    path("", graphiql),
    path('admin/', admin.site.urls),
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        'api/v1/',
        include((class_room.urls, 'class_room'), namespace='class_room')
    ),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    urlpatterns += \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
