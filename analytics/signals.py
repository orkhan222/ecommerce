from django.dispatch import Signal

object_viewd_signal = Signal(providing_args=['instance','request'])