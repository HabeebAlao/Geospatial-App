"""
URL configuration for geodjango_tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import re_path, include, path
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from user_location import views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # user_location urls
    re_path(r"^serviceworker\.js$", views.service_worker, name="serviceworker"),
    re_path(r"^manifest\.json$", views.manifest, name="manifest"),
    path("offline/", views.offline, name="offline"),
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('events/', views.events, name="events"),
    path('events/<slug:slug>/', views.events, name='event_detail'),
    path('profile/', views.profile, name="profile"),
    path('edit_event/', views.edit_event, name='edit_event'),
    path('update_going/', views.update_going, name="update_going"),
    path('location_geocode/', views.location_geocode, name='location_geocode'),
    path('api-auth/', include('rest_framework.urls')),
    # path('', include('myApiApp.urls'))
]
