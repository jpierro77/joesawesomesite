from configparser import RawConfigParser

config = RawConfigParser()
config.read('../joesawesomesite/settings.ini')
print(config)
print(config.sections())
TWITTER_ACCESS_KEY = config.get('twitter_api', 'twitter_access_key')
TWITTER_ACCESS_SECRET = config.get('twitter_api', 'twitter_access_secret')

print(TWITTER_ACCESS_KEY)