from django.apps import AppConfig


class AccomodationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accomodations'
    verbose_name = 'Student Accommodations'

    def ready(self):
        try:
            import accomodations.signals
        except ImportError:
            pass
