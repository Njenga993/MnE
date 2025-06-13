from django.urls import path
from core.views import html_login_view, login_user, register_user, get_profile, logout_user

urlpatterns = [
    path('', html_login_view, name='login'),  # Root URL opens login page
    path('api/login/', login_user, name='api_login'),  # Your existing API login
    path('api/register/', register_user, name='register_user'),
    path('api/profile/', get_profile, name='get_profile'),
    # Add dashboard path as well:
    path('Login/', login_user, name='login_user'), 
    path('logout/', logout_user, name='logout'),
]
