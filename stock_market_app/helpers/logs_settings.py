import logging 

def get_logger():
    # Set up loggings
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/app_three.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)