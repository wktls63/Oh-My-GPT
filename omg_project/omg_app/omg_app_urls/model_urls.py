from django.urls import path
from ..omg_app_views import model_views

urlpatterns = [
    path('upload_model/', model_views.upload_model, name='upload_model'),
    path('write/', model_views.upload_model, name='write'),

]