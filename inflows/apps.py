from django.apps import AppConfig


class InflowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inflows'

    def ready(self):
        import importlib
        importlib.import_module('inflows.signals')
