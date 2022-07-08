import datetime
import random
import string
import os
from app_logging import logObject

# saves message to today's folder with datetime and random str name


def save_message_to_file(save_path, message, return_file_path):
    # random str generator
    random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
    # filename with random str
    filename = f'{datetime.datetime.now().strftime("%Y_%m_%d %H-%M-%S-%f")} - {random_str}.txt'
    today_date = datetime.date.today()
    # combine path and filename
    filename_with_path = f'{save_path}/Saved_Messages/{today_date}/{filename}'
    # creates directory if it does not exist already
    os.makedirs(os.path.dirname(filename_with_path), exist_ok=True)
    with open(filename_with_path, 'w') as file:
        file.write(str(message))
    logObject.warning(f'        Message save to file: {filename_with_path}')
    if return_file_path:
        return filename_with_path, filename
