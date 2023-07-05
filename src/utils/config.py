import yaml

with open('./config/config.yaml') as config:
    try:
        data = yaml.safe_load(config)
    except yaml.YAMLError as e:
        print(e)

SCHEDULED_POSTS = data['scheduled_posts']
TIMEZONE = data['timezone']
URI = data['lemmy_base_uri']