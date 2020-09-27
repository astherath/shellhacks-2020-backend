import os
import geopy

SECRET_KEY = os.environ["SHELLHACKS_SECRET_KEY"]
ALGORITHM = "HS256"

DB_URI = os.environ["SHELLHACKS_MONGO_URI"]

ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1:*",
    "http://127.0.0.1",
    "127.0.0.1",
    "http://localhost:8080",
    "http://localhost:*",
    "localhost:8080",
    "http://localhost",
    "localhost",
]

ALLOWED_HOSTS = [
    "shellhacks-2020.herokuapp.com",
    "www.shellhacks-2020.herokuapp.com",
    "52.150.19.14:8080",
    "52.150.19.14",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost",
    "http://localhost",
    "localhost",
]

ALLOWED_HEADERS = ["*", "x-requested-with"]
API_TITLE = "API Gateway"
API_VERSION = "v.1.0"
API_DESCRIPTION = "HTTP1 REST API Gateway"

AGENT = geopy.Nominatim(user_agent="default")
