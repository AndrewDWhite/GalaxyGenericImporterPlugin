import logging

async def update_cache(self, my_cache_update):
    #Potential race condition here probably want to add semaphores on cache writes or refactor
    self.backend.library_lock.acquire()
    try:
        logging.debug("locked for cache updates")
        self.backend.local_game_cache = my_cache_update
        self.backend.my_game_lister.write_to_cache(my_cache_update)
    finally:
        self.backend.library_lock.release()
        logging.debug("lock released for cache updates")
        
async def update_cache_time(self, my_cache_update, cache_filepath):
    #Potential race condition here probably want to add semaphores on cache writes or refactor
    self.backend.library_lock.acquire()
    try:
        logging.debug("locked for time updates")
        self.backend.local_time_cache = my_cache_update
        self.backend.my_game_lister.write_to_cache_file(my_cache_update, cache_filepath)
    finally:
        self.backend.library_lock.release()
        logging.debug("lock released for time updates")


