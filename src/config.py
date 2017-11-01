import os
import keys

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = 'secret'

DATA_BACKEND = 'datastore'

PROJECT_ID = 'simplejournal-184519'

DEBUG = False
ADMINS = frozenset([keys.EMAIL])


# Mongo configuration
# If using mongolab, the connection URI is available from the mongolab control
# panel. If self-hosting on compute engine, replace the values below.
MONGO_URI = \
    'mongodb://user:password@host:27017/database'
