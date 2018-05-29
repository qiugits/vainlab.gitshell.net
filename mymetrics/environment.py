import os


def when_development():
    env = os.environ.get('WEB_ENVIRONMENT', '')
    return True if env == 'development' else False
