import os
from urllib.parse import urlparse

# bot interval and timeout
bot_interval = 3
bot_timeout = 30
current_result = ""

# set environment variables
# bot api
api_key = "1314384954:AAHcFphPjJaMK5oxJYEDDjEauhygCZzyMD4"

# database details
url = urlparse.urlparse(os.environ['DATABASE_URL'])
db_user = url.username
db_password = url.password
db_host = url.hostname
db_port = url.port
db_name = url.path[1:]

# us sports news
ussports = "http://newsapi.org/v2/top-headlines?country=us&q=sports&apiKey=14404d1267a94b8fa3d50e5364ed10d4"

# uk sports news
uksports = "http://newsapi.org/v2/top-headlines?country=uk&q=sports&apiKey=14404d1267a94b8fa3d50e5364ed10d4"
