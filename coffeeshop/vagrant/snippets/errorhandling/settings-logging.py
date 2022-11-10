# Add this code to settings.py to log errors to the console.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler"
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO"
        }
    }
}
