from django.apps import AppConfig
from django.core.checks import register, Error
from django.conf import settings


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"


@register
def check_backend_settings(app_configs, **kwargs):
    errors = []
    if (
        "authentication.backends.EmailModelBackend"
        not in settings.AUTHENTICATION_BACKENDS
    ):
        errors.append(
            Error(
                "EmailModelBackend not found in AUTHENTICATION_BACKENDS",
                hint="Add 'authentication.backends.EmailModelBackend' to AUTHENTICATION_BACKENDS in settings.py",
                id="authentication.E001",
            )
        )
    return errors
