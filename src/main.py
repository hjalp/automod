import logging
import os
import sys
import time

from dotenv import load_dotenv

from modules.scheduler import Scheduler
from utils.config import URI, TIMEZONE, SCHEDULED_POSTS
from utils.safe_scheduler import SafeScheduler

load_dotenv()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=os.getenv('LOGLEVEL', logging.INFO))

if __name__ == '__main__':
    for var_name in ['LEMMY_USERNAME', 'LEMMY_PASSWORD']:
        if not os.getenv(var_name):
            logging.error(f'Error: {var_name} environment variable is not set.')
            sys.exit(1)

    USERNAME = os.getenv('LEMMY_USERNAME')
    PASSWORD = os.getenv('LEMMY_PASSWORD')

    scheduler = SafeScheduler()

    post_scheduler = Scheduler(scheduler=scheduler, uri=URI, timezone=TIMEZONE, username=USERNAME, password=PASSWORD)
    post_scheduler.schedule_posts(SCHEDULED_POSTS)

    while True:
        scheduler.run_pending()
        time.sleep(1)