# __init__.py for dashboard
from django.apps import AppConfig
# dashboard/__init__.py
class DashboardConfig(AppConfig):
    name = 'dashboard'
    verbose_name = 'Dashboard Management'

    def ready(self):
        # Import signals or any other startup code here
        import dashboard.signals  # Assuming you have a signals.py for handling model signals
        # You can also import other modules or perform any initialization tasks here
        print("Dashboard app is ready.")
        # Example: Registering model signals
        # from . import signals  # Uncomment if you have a signals.py file
        