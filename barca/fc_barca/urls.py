from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from users import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('squad/', views.squad, name='squad'),
    path('auth/', views.auth, name='auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('feedback/', views.feedback_view, name='feedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)