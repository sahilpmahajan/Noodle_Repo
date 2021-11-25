
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = 'chat'

urlpatterns = [
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
