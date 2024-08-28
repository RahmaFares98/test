from django.apps import AppConfig


class NeedForSpeedAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'need_for_speed_app'

    def ready(self):
        import need_for_speed_app.signals

    
