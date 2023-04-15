import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    # _db_name: str = os.getenv('DB_NAME')
    db_host: str = os.getenv('DB_HOST')
    vantage_apikey: str = os.getenv('VANTAGE_APIKEY')

    # @property
    # def db_name(self):
    #     if os.getenv('RUN_ENV') == 'test':
    #         return 'test_' + self._db_name

    #     return self._db_name
