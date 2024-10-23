import os
from os import getenv

from dotenv import load_dotenv

from OWNER import (
    BOT_TOKEN,
    CHANNEL,
    DATABASE,
    GROUP,
    LOGS,
    OWNER,
    OWNER_NAME,
    VID_SO,
    VIDEO,
)

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
user = {}
call = {}
dev = {}
logger = {}
logger_mode = {}
botname = {}
appp = {}
helper = {}


API_ID = int(getenv("API_ID", "12962251"))
API_HASH = getenv("API_HASH", "b51499523800add51e4530c6f552dbc8")
BOT_TOKEN = BOT_TOKEN
MONGO_DB_URL = DATABASE
OWNER = OWNER
OWNER_NAME = OWNER_NAME
CHANNEL = CHANNEL
GROUP = GROUP
LOGS = LOGS
VIDEO = VIDEO
VID_SO = VID_SO
