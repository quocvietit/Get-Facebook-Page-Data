import os

__APP_ID = os.environ.get('APP_ID')
__APP_SECRET = os.environ.get('APP_SECRET')
__TOKEN = "{}|{}"


# Get My App ID
def app_id():
    return __APP_ID


# Get My App secret
def app_secret():
    return __APP_SECRET


# Get Token
# return  [AppID]|[App Secret ]
def token():
    return __TOKEN.format(__APP_ID, __APP_SECRET)
