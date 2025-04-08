from django.urls import path
from users.views import register, login, get_user_view, search_users_view


urlpatterns = [
    path('user/register', register),
    path('login', login),
    path('user/get/<int:user_id>', get_user_view),
    path('user/search', search_users_view),
]
