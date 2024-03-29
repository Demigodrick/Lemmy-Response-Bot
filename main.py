from bot_code import login, check_dbs, check_comments, clear_notifications, check_pms
from config import settings
import logging
import schedule
import time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Hello! Bot starting...")
logging.info("Bot Version 0.0.5")

if __name__ == "__main__":
    
    #run once
    login()
    check_dbs()

    #variable 
    schedule.every(settings.POLL_FREQ).seconds.do(check_comments)
    
    #minutes
    schedule.every(1).minute.do(check_pms)
    
    #minutes
    schedule.every(10).minutes.do(clear_notifications)


while True:
    schedule.run_pending()
    time.sleep(1)
