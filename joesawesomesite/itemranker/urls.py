from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='itemranker'),
    path('twitterpost/', views.twitterpost, name ="twitterpost"),
    path('callback/', views.callback, name = 'callback'),
    path('savelist/', views.savelist, name='savelist'),
    path('personallist/<int:list_id_arg>', views.personal_list_display, name='personal_list_display'),
    path('personallist/', views.personal_list_display, name='personal_list_display'),
    path('masterlist/<int:list_id_arg>', views.master_list_display, name='master_list_display'),
    path('masterlist/', views.master_list_display, name='master_list_display'),
    path('addvote/<int:master_list_id>/<int:item_id>', views.add_vote, name = "add_vote"),
    path('additem/<int:master_list_id>', views.add_item, name = "add_item"),
    path('deleteranklist/', views.delete_ranklist, name='deleteranklist'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


