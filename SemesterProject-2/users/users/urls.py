from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('', views.index, first_name='index'),
    path('<int:user_id>', views.info, name='info'),
]