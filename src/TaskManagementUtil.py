import logging
import asyncio
import json
from datetime import datetime
from TimeCache import finished_game_run

async def shutdown_tasks(self, tasks):
        for task in tasks:
            logging.debug("canceling")
            logging.debug(task)
            try:
                await task.cancel()
            except asyncio.CancelledError:
                logging.error('cancel_me(): cancel')
        
        for task in tasks:
            while not task.done:
                logging.debug("waiting for")
                logging.debug(tasks)
                await asyncio.sleep(1)
                
async def time_tracking(self, my_threads):
    #for tracking time
    my_threads_to_remove = []
    logging.debug("thread size")
    logging.debug(len(my_threads))
    for my_current_thread in my_threads:
        if not my_current_thread.is_alive():
            logging.debug("thread not alive")
            my_thread_name = my_current_thread.name
            logging.debug(my_thread_name)
            logging.debug(my_thread_name)
            my_dictionary_values = json.loads(my_thread_name)
            await finished_game_run(self, datetime.fromisoformat(my_dictionary_values["time"]),my_dictionary_values["id"], self.backend.local_time_cache)
            my_threads_to_remove.append(my_current_thread)
    for my_thread_to_remove in my_threads_to_remove:
        logging.debug("thread removed")
        my_threads.remove(my_thread_to_remove)

