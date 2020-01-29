class Config(object):
	SECRET_KEY = 'PSuSmgGYziSf0qgUOM7E0QW5KlL3gsHd'

class LocalConfig(Config):
	HOST = '0.0.0.0'
	PORT = 3200
	DEBUG = True
	RELOAD = True

Conf = LocalConfig