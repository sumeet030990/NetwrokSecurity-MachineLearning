import logging
import os
from datetime import datetime

LOG_FILE_INFO=f"{datetime.now().strftime('%d_%m_%Y')}.log"
LOG_FILE_INFO_PATH = os.path.join(os.getcwd(),"logs",LOG_FILE_INFO)

# Creates a new file
with open(LOG_FILE_INFO_PATH, 'a') as fp:
    pass


logging.basicConfig(
    filename=LOG_FILE_INFO_PATH,
    format="************************************************************ \n \n Timestamp: [ %(asctime)s ]|| File name: %(name)s - Line: %(lineno)d - %(levelname)s - %(message)s \n",
    datefmt="%d_%m_%Y || %I:%M:%S %p",  # This sets the date format
    level=logging.INFO,
)
