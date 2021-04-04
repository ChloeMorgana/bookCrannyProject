from django.contrib import admin
from django.urls import path
from django.urls import include
from bookCranny import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'), 
    path('bookcranny/', include('bookCranny.urls')), 
    path('admin/', admin.site.urls),
    path('accounts/register/', views.register, name = 'register'),
    path('accounts/', include('registration.backends.simple.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
