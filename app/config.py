import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'DO_NOT_USE_IN_PROD'
	CACHE_TYPE = "SimpleCache"
	CACHE_DEFAULT_TIMEOUT= 300