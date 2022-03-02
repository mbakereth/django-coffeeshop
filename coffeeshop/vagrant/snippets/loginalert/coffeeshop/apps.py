from django.apps import AppConfig


class CoffeeshopConfig(AppConfig):
    name = 'coffeeshop'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
