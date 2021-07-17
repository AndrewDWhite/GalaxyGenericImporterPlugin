import logging
from datetime import datetime
import math

async def time_delta_calc_minutes(last_update):
    logging.debug("time delta calculating")
    current_time = datetime.now()
    logging.debug(current_time)
    logging.debug(last_update)
    time_delta = (current_time - last_update)
    time_delta_seconds = time_delta.total_seconds()
    return math.ceil(time_delta_seconds/60)