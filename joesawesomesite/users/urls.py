from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('profile/<str:username>/', views.user_profile, name="user_profile"),
    path('profile/', views.user_profile, name="user_profile"),
    path('edit/', views.edit_profile, name="edit_profile"),
    path('login/', views.login, name="login"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)