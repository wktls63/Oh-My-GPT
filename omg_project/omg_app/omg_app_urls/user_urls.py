from django.urls                    import path, include
from ..omg_app_views                import user_views
from ..omg_app_views.user_views     import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('email_verify/<str:token>/', user_views.verify_email, name='email_verify'),
    path("auth/refresh/", TokenRefreshView.as_view()),                                  # jwt 토큰 재발급
]