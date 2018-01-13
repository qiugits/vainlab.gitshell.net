import os


def if_is_development():
    try:
        env = os.environ['WEB_ENVIRONMENT']
    except:
        env = ''
    return True if env == 'development' else False
