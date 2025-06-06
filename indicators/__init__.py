# __init__.py for indicators
from django.apps import AppConfig
class IndicatorsConfig(AppConfig):
    name = 'indicators'
    verbose_name = 'Indicators Management'

    def ready(self):
        # Import signals or any other startup code here
        import indicators.signals  # Assuming you have a signals.py for handling model signals
        # You can also import other modules or perform any initialization tasks here
        print("Indicators app is ready.")
        # Example: Registering model signals
        # from . import signals  # Uncomment if you have a signals.py file