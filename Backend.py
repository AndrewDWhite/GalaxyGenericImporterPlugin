from galaxy.api.types import Authentication, LocalGame

from ListGames import ListGames
from TaskManagementUtil import time_tracking
from TimeUtils import time_delta_calc_minutes
from UpdatesQueueUtil import prepare_to_send_my_updates

import logging
from datetime import datetime
import threading
import queue
import asyncio

class Backend():
    
    def __init__(self):
        logging.debug("init backend")
        self.backend_setup = False
        self.last_update = datetime.now()
        self.my_imported_owned = False
        self.my_imported_local = False
        self.my_game_lister =  ListGames()
        self.cache_times_filepath = self.my_game_lister.cache_filepath+"-times"
        self.local_time_cache = []
        self.library_lock = threading.Lock()
        logging.debug("Setup queues")
        self.my_queue_update_local_game_status = queue.Queue()
        self.my_queue_add_game = queue.Queue()
        self.my_queue_update_game_time = queue.Queue()
        self.my_queue_folder_awaiting_scan = queue.Queue()
        self.my_authenticated = False
        self.not_updating_list_scan = False
        logging.debug("Backend init completed sucessfuly")
        
    async def setup(self, configuration):
        logging.debug("Setup backend")
        logging.debug("cache")
        self.local_game_cache = await self.my_game_lister.read_from_cache()
        
        logging.debug("preparing to seed changes")
        await self.seedChanges(self.local_game_cache)

        my_cache_exists = await self.my_game_lister.cache_exists_file(self.cache_times_filepath)
        if my_cache_exists:
            self.local_time_cache = await self.my_game_lister.read_from_cache_filename(self.cache_times_filepath)
        
        self.library_run = True       
        self.not_updating_list_scan = True
        self.backend_setup = True
        logging.debug("backend started up")
        
    async def seedChanges(self, cache):
        for my_game in cache:
            logging.debug(my_game)
            self.my_queue_update_local_game_status.put(LocalGame(my_game["hash_digest"], my_game["local_game_state"]))
        
async def shutdown_library(self):
    logging.debug("shutdown folder listeners")
    await self.backend.my_game_lister.shutdown_folder_listeners()
    
    logging.debug("Library update in progress?")
    self.backend.library_run= False
    #loop = asyncio.get_event_loop()
    #loop.close() 
    
    while (self.my_library_thread.is_alive()):
        await asyncio.sleep(1)
    
    #self.my_library_thread.join()
    #for my_current_future in self.my_tasks:
    #    if not my_current_future.done():
    #        my_current_future.cancel() 
    logging.debug("done with shutdown_library")

#Will cause issues it not called from initial thread
async def send_events(self):
    logging.debug("sending events to galaxy")
    logging.debug("my_queue_add_game length")
    logging.debug(self.backend.my_queue_add_game.empty())
    logging.debug(self.backend.my_queue_add_game.qsize())
    countDelivered = 0
    while not self.backend.my_queue_add_game.empty() and countDelivered < 101:
        my_game_sending = self.backend.my_queue_add_game.get()
        logging.debug(my_game_sending)
        self.add_game(my_game_sending)
        countDelivered = countDelivered + 1
    
    logging.debug("my_queue_update_local_game_status update length")
    logging.debug(self.backend.my_queue_update_local_game_status.empty())
    logging.debug(self.backend.my_queue_update_local_game_status.qsize()) 
    countDelivered = 0   
    while not self.backend.my_queue_update_local_game_status.empty() and countDelivered < 101:
        my_game_sending = self.backend.my_queue_update_local_game_status.get()
        logging.debug(my_game_sending)
        self.update_local_game_status(my_game_sending)
        countDelivered = countDelivered + 1
  
    logging.debug("my_queue_update_game_time update length")
    logging.debug(self.backend.my_queue_update_game_time.empty())
    logging.debug(self.backend.my_queue_update_game_time.qsize()) 
    countDelivered = 0        
    while not self.backend.my_queue_update_game_time.empty() and countDelivered < 101:    
        my_game_sending = self.backend.my_queue_update_game_time.get()
        logging.debug(my_game_sending)
        self.update_game_time(my_game_sending)
        countDelivered = countDelivered + 1


def library_thread(self):
    logging.debug("TODO start up thread for library, we may wait for the backend to startup")
    #Wait for backend to be setup and then we can go
    while not self.backend.backend_setup:
        pass
    self.backend.library_run = True
    
    if not self.my_library_started:
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #asyncio.get_event_loop()
        logging.debug("TODO library loop: We haven't started it yet so lets do that")
        
#         try:
#             loop = asyncio.get_event_loop()
#             logging.debug("library thread has loop and starting")
#             my_task = asyncio.create_task(update_local_games(self, self.configuration.my_user_to_gog, self.backend.my_game_lister) )
#             self.my_tasks.append(my_task)
#         except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run((update_local_games(self, self.configuration.my_user_to_gog, self.backend.my_game_lister) ))      

        self.my_library_started = True
        logging.debug("Finished start up thread for library")

async def tick_async(self):   
    while(self.keep_ticking):
        logging.debug("backend running for us to get what we need from it?")
        logging.debug(self.backend.backend_setup)
        logging.debug("System logged in for us to bother with this?")
        logging.debug(self.backend.my_authenticated)
        if self.backend.backend_setup and self.backend.my_authenticated:
            #if self.my_library_thread == None:
            #logging.debug("lib?")
            #logging.debug(self.my_library_thread.is_alive())
            #try:
            await send_events(self) 
            #finally:
            #    loop.close()  
            #try:
            await time_tracking(self, self.my_threads)            #finally:
            #    my_loop.close()   
        await asyncio.sleep(1) 

async def update_local_games(self, username, my_game_lister):
    not_run = True
    logging.debug("update_local_games")
    logging.debug(self.backend.library_run)
    while(self.backend.library_run):
        logging.debug("checking for back end library ready")
        logging.debug(self.backend.my_authenticated and self.backend.my_imported_owned and self.backend.my_imported_local)
        if self.backend.my_authenticated and self.backend.my_imported_owned and self.backend.my_imported_local:
            #delta is calculated to ensure that we only run expensive operation no more than once a minute
            time_delta_minutes = await time_delta_calc_minutes(self.backend.last_update)
            logging.debug("delta")
            logging.debug(time_delta_minutes)
            logging.debug("not run?")
            logging.debug(not_run)
            #TODO could be more specific about rescans
            logging.debug("update list not pending?")
            logging.debug(self.backend.my_queue_folder_awaiting_scan.empty())
            logging.debug("I am not updating?")
            logging.debug(self.backend.not_updating_list_scan)
            logging.debug("lets go in here for a scan?")
            logging.debug(not_run)
            logging.debug(not self.backend.my_queue_folder_awaiting_scan.empty() and self.backend.not_updating_list_scan and time_delta_minutes>1)
            logging.debug(not_run or (not self.backend.my_queue_folder_awaiting_scan.empty() and self.backend.not_updating_list_scan and time_delta_minutes>1))
            if (not_run or (not self.backend.my_queue_folder_awaiting_scan.empty() and self.backend.not_updating_list_scan and time_delta_minutes>1)):
                logging.debug("Starting a full scan")
                self.backend.not_updating_list_scan = False
                while not self.backend.my_queue_folder_awaiting_scan.empty(): 
                    #TODO can limit to these
                    logging.debug(self.backend.my_queue_folder_awaiting_scan.get())
                if not_run:
                    logging.debug("setting up folder listeners")
                    await my_game_lister.setup_folder_listeners(self.backend.my_queue_folder_awaiting_scan)
                not_run = False
                self.backend.last_update = datetime.now()
                logging.debug("get local updates")
                new_local_games_list = await my_game_lister.list_all_recursively(username)
                logging.debug("Got new List")
                await prepare_to_send_my_updates(self, new_local_games_list, self.backend.local_game_cache)
                self.backend.not_updating_list_scan = True
                
        logging.debug("sleepy")
        await asyncio.sleep(10)
    #tasks = [t for t in asyncio.all_tasks() if t is not
    #         asyncio.current_task()]
    #for task in tasks:
    #    logging.debug("canceling")
    #    task.cancel()
    #for task in tasks:
    #        while not task.done:
    #            logging.debug("waiting for")
    #            logging.debug(tasks)
    logging.debug("bye")

async def do_auth(self, username):    
    logging.debug("Auth request started")
    user_data = {}
    logging.debug(username)
    user_data['username'] = username       
    self.store_credentials(user_data)
    self.backend.my_authenticated = True
    return Authentication('importer_user', user_data['username'])

