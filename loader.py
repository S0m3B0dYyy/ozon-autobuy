import configparser
import os

config = configparser.ConfigParser()
path = os.path.join(os.getcwd(), 'settings.ini')
config.read(path, 'utf-8')

SKU_ID: int = int(config['MAIN']['SKU_ID'])
SKU_QUANTITY: int = int(config['MAIN']['SKU_QUANTITY'])
ACCESS_TOKEN: str = config['MAIN']['ACCESS_TOKEN']
REFRESH_TOKEN: str = config['MAIN']['REFRESH_TOKEN']
ABT_DATA: str = config['MAIN']['ABT_DATA']
ORDER_ATTEMPTS: int = int(config['MAIN']['ORDER_ATTEMPTS'])
ORDER_INTERVAL: float = float(config['MAIN']['ORDER_INTERVAL'])
ADD_TO_CART: float = float(config['MAIN']['ADD_TO_CART'])

HOURS: int = int(config['START_TIME']['HOURS'])
MINUTES: int = int(config['START_TIME']['MINUTES'])
SECONDS: int = int(config['START_TIME']['SECONDS'])
MILLISECONDS: int = int(config['START_TIME']['MILLISECONDS'])

USE_PROXY: int = int(config['REQUESTS']['USE_PROXY'])
REQUEST_ATTEMPTS: int = int(config['REQUESTS']['REQUEST_ATTEMPTS'])
REQUEST_INTERVAL: float = float(config['REQUESTS']['REQUEST_INTERVAL'])

USE_MEASURING: int = int(config['DEBUG']['USE_MEASURING'])
USE_START_TIME: int = int(config['DEBUG']['USE_START_TIME'])
