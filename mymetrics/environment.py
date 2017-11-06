import os


def if_is_development():
    try:
        GA_TRACKING_ID = os.environ['GA_TRACKING_ID']
    except:
        GA_TRACKING_ID = ''
    env = 'production' if GA_TRACKING_ID else 'development'
    return True if env == 'development' else False
