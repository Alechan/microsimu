import os
from dotenv import load_dotenv

from microsimu.settings import BASE_DIR

PROD_ENV_FILE_PATH = BASE_DIR / ".env.prod"
DEV_ENV_FILE_PATH  = BASE_DIR / ".env.dev"

env_file = PROD_ENV_FILE_PATH if os.path.isfile(PROD_ENV_FILE_PATH) else DEV_ENV_FILE_PATH
if not os.path.isfile(DEV_ENV_FILE_PATH):
    raise EnvironmentError("Please provide a .env.dev file or a .env.prod file.")

load_dotenv(env_file)

pass