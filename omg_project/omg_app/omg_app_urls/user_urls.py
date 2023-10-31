from django.urls                    import path, include
from ..omg_app_views                import user_views
from ..omg_app_views.user_views     import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('signup/', user_views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', user_views.verify_email, name="activate"),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/refresh/", TokenRefreshView.as_view()),                                    # jwt 토큰 재발급
]