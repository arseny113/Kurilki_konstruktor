from environs import Env
from ConfigFromJsonToDict import config_data
env = Env()
env.read_env()

service_settings = config_data['service_settings']

BOT_TOKEN = service_settings['bot_token']
SUPPORT_IDS = service_settings['support_ids']
MANAGER_ID = service_settings['manager_id']

DB_USER = service_settings['db_user']
DB_PASS = service_settings['db_pass']
DB_HOST = service_settings['db_host']
DB_PORT = service_settings['db_port']
DB_NAME = service_settings['db_name']


def database_url_asyncpg(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME):
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


database_url = database_url_asyncpg(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
