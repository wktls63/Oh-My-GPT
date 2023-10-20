from django.urls import path
from ..omg_app_views import user_views

urlpatterns = [
    path('signup/', user_views.signup, name='signup'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('email_verify/<str:token>/', user_views.verify_email, name='email_verify'),
]