from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import login_user

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    path('', login_user, name='login'),  # ✅ This handles the root URL

    # API Routes (versioned for future scalability)
    path('api/v1/logframe/', include('logframe.urls')),
    path('api/v1/mobile/', include('mobile_api.urls')),
    path('api/v1/indicators/', include('indicators.urls')),

    # Additional Modules (Uncomment when used)
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/comments/', include('comments.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api/v1/tasks/', include('tasks.urls')),
    path('api/v1/core/', include('core.urls')),  # For auth, users, profiles
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)