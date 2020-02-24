from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='caloriesindex'),
    path('updatehealth/', views.update_health_info, name="updatehealthinfo"),
    path('newday/', views.new_day, name="newday"),
    path('loginredirect/', views.login_redirect, name='login_redirect')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
