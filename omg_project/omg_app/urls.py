from . import views
from django.urls import path, include
from .omg_app_urls.chat_urls import urlpatterns as chat_urlpatterns


urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat, name='chat'),
    path('write/', views.write, name='write'),
    path('loading/', views.loading, name='loading'),
    path('payment/', views.payment, name='payment'),
    path('intro/', views.intro, name='intro'),
    path('login/', views.login, name='login'),
    path('center_write/', views.center_write, name='center_write'),
    path('center/', views.center, name='center'),
]


# user_views.py
urlpatterns += [
    
]

# chat_views.py
urlpatterns += [
    path('chat/', include((chat_urlpatterns, 'chat')))
]
