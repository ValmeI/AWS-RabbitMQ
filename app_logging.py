import logging
import datetime
import os

# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’).
# The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

# creates a new folder every day, where give day logs go to
today_date = datetime.date.today()
log_folder = str(today_date)
filename = f'{today_date}.log'
log_file_path = f'Logs/{log_folder}/{today_date}.log'

# creates folder if it does not exist. Used for in logging to file system.
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# with handler, I can log to file and to console at the same time
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()]
                    )


logObject = logging.getLogger()
# logger to WARNING
logObject.setLevel(logging.WARNING)
