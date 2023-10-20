from . import views
from django.urls import path, include

from .views import SubScriptionAPIViewp

from .omg_app_urls.chat_urls import urlpatterns as chat_urlpatterns
from .omg_app_urls.user_urls import urlpatterns as user_urlpatterns
from .omg_app_urls.model_urls import urlpatterns as model_urlpatterns

api_patterns = [

    # api url
    path('subscription', SubScriptionAPIViewp.as_view()),
]




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

    # api
    path('api/', include(api_patterns)),
]


# user_views.py
urlpatterns += [
    path('login/', include((user_urlpatterns))),
]


# chat_views.py
urlpatterns += [
    path('chat/', include((chat_urlpatterns, 'chat')))
]

# model_views.py
urlpatterns += [
    path('model/', include((model_urlpatterns, 'model')))
]