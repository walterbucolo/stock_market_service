import logging 
from datetime import datetime
import os



def get_logger():
    # Set up loggings
    folder_name = 'file_logs'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    today = str(datetime.now().date())
    
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("{}/log-{}.log".format(folder_name, today)),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)