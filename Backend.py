from galaxy.api.consts import LocalGameState
from galaxy.api.types import Authentication, Game, LocalGame, LicenseInfo, LicenseType, GameTime

from ListGames import ListGames

import logging
import os
from escapejson import escapejson
import json
from datetime import datetime
import math
import threading
import queue
import asyncio

class Backend():
    
    def __init__(self):
        logging.info("init backend")
        self.backend_setup = False
        self.last_update = datetime.now()
        self.my_imported_owned = False
        self.my_imported_local = False
        self.my_game_lister =  ListGames()
        self.cache_times_filepath = self.my_game_lister.cache_filepath+"-times"
        self.local_time_cache = []
        self.library_lock = threading.Lock()
        logging.info("Setup queues")
        self.my_queue_update_local_game_status = queue.Queue()
        self.my_queue_add_game = queue.Queue()
        self.my_queue_update_game_time = queue.Queue()
        self.my_queue_folder_awaiting_scan = queue.Queue()
        self.my_authenticated = False
        self.not_updating_list_scan = False
        logging.info("Backend init completed sucessfuly")
        
    async def setup(self, configuration):
        logging.info("Setup backend")
        logging.info("cache")
        self.local_game_cache = await self.my_game_lister.read_from_cache()
        
        logging.info("preparing to seed changes")
        await self.seedChanges(self.local_game_cache)

        my_cache_exists = await self.my_game_lister.cache_exists_file(self.cache_times_filepath)
        if my_cache_exists:
            self.local_time_cache = await self.my_game_lister.read_from_cache_filename(self.cache_times_filepath)
        
        self.library_run = True       
        self.not_updating_list_scan = True
        self.backend_setup = True
        logging.info("backend started up")
        
    async def seedChanges(self, cache):
        for my_game in cache:
            logging.info(my_game)
            self.my_queue_update_local_game_status.put(LocalGame(my_game["hash_digest"], my_game["local_game_state"]))
        
async def shutdown_library(self):
    logging.info("shutdown folder listeners")
    await self.backend.my_game_lister.shutdown_folder_listeners()
    
    logging.info("Library update in progress?")
    self.backend.library_run= False
    #loop = asyncio.get_event_loop()
    #loop.close() 
    
    while (self.my_library_thread.is_alive()):
        await asyncio.sleep(1)
    
    #self.my_library_thread.join()
    #for my_current_future in self.my_tasks:
    #    if not my_current_future.done():
    #        my_current_future.cancel() 
    logging.info("done with shutdown_library")

async def time_tracking(self, my_threads):
    #for tracking time
    my_threads_to_remove = []
    logging.info("thread size")
    logging.info(len(my_threads))
    for my_current_thread in my_threads:
        if not my_current_thread.is_alive():
            logging.info("thread not alive")
            my_thread_name = my_current_thread.name
            logging.info(my_thread_name)
            logging.info(my_thread_name)
            my_dictionary_values = json.loads(my_thread_name)
            await finished_game_run(self, datetime.fromisoformat(my_dictionary_values["time"]),my_dictionary_values["id"], self.backend.local_time_cache)
            my_threads_to_remove.append(my_current_thread)
    for my_thread_to_remove in my_threads_to_remove:
        logging.info("thread removed")
        my_threads.remove(my_thread_to_remove)
        
async def create_game(game):
    my_hash = escapejson(game["hash_digest"])
    my_game_name = escapejson(game["game_name"])
    return Game(my_hash, my_game_name, None, LicenseInfo(LicenseType.SinglePurchase))

async def prepare_to_send_my_updates(self, new_local_games_list, local_game_cache):
    logging.info("sending updates")
    for entry in new_local_games_list:
        if("local_game_state" not in entry):
            #If we haven't added the game and we want it to count as installed
            if (entry["gameShouldBeInstalled"]):
                logging.info("Here and installed")
                entry["local_game_state"]=LocalGameState.Installed
            else:
                logging.info("Here but not installed")
                entry["local_game_state"]=LocalGameState.None_
    state_changes = await get_state_changes(local_game_cache, new_local_games_list)
    await setup_queue_to_send_those_changes(self, new_local_games_list, state_changes["old"], state_changes["new"])
    await update_cache(self, new_local_games_list)

#Will cause issues it not called from initial thread
async def send_events(self):
    logging.info("sending events to galaxy")
    logging.info("my_queue_add_game length")
    logging.info(self.backend.my_queue_add_game.empty())
    logging.info(self.backend.my_queue_add_game.qsize())
    while not self.backend.my_queue_add_game.empty():
        my_game_sending = self.backend.my_queue_add_game.get()
        logging.info(my_game_sending)
        self.add_game(my_game_sending)
    
    logging.info("my_queue_update_local_game_status update length")
    logging.info(self.backend.my_queue_update_local_game_status.empty())
    logging.info(self.backend.my_queue_update_local_game_status.qsize())    
    while not self.backend.my_queue_update_local_game_status.empty():
        my_game_sending = self.backend.my_queue_update_local_game_status.get()
        logging.info(my_game_sending)
        self.update_local_game_status(my_game_sending)
  
    logging.info("my_queue_update_game_time update length")
    logging.info(self.backend.my_queue_update_game_time.empty())
    logging.info(self.backend.my_queue_update_game_time.qsize())      
    while not self.backend.my_queue_update_game_time.empty():    
        my_game_sending = self.backend.my_queue_update_game_time.get()
        logging.info(my_game_sending)
        self.update_game_time(my_game_sending)

async def removed_games(self, old_dict, new_dict):
    # removed games
    for my_id in (old_dict.keys() - new_dict.keys()):
        logging.info("removed")
        self.backend.my_queue_update_local_game_status.put(LocalGame(my_id, LocalGameState.None_))

async def added_games(self, new_list, old_dict, new_dict):
    # added games
    for local_game in new_list:
        if ("hash_digest" in local_game) and (local_game["hash_digest"] in (new_dict.keys() - old_dict.keys())):
            logging.info("added")
            my_created_game = await create_game(local_game)
            self.backend.my_queue_add_game.put(my_created_game)
            self.backend.my_queue_update_local_game_status.put(LocalGame(local_game["hash_digest"], local_game["local_game_state"]))

async def state_changed(self, old_dict, new_dict):
    # state changed
    for my_id in new_dict.keys() & old_dict.keys():
        if new_dict[my_id] != old_dict[my_id]:
            logging.info("changed")
            self.backend.my_queue_update_local_game_status.put(LocalGame(my_id, new_dict[my_id]))

def library_thread(self):
    logging.info("TODO start up thread for library, we may wait for the backend to startup")
    #Wait for backend to be setup and then we can go
    while not self.backend.backend_setup:
        pass
    self.backend.library_run = True
    
    if not self.my_library_started:
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #asyncio.get_event_loop()
        logging.info("TODO library loop: We haven't started it yet so lets do that")
        
#         try:
#             loop = asyncio.get_event_loop()
#             logging.info("library thread has loop and starting")
#             my_task = asyncio.create_task(update_local_games(self, self.configuration.my_user_to_gog, self.backend.my_game_lister) )
#             self.my_tasks.append(my_task)
#         except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run((update_local_games(self, self.configuration.my_user_to_gog, self.backend.my_game_lister) ))      

        self.my_library_started = True
        logging.info("Finished start up thread for library")

async def tick_async(self):   
    while(self.keep_ticking):
        logging.info("backend running for us to get what we need from it?")
        logging.info(self.backend.backend_setup)
        logging.info("System logged in for us to bother with this?")
        logging.info(self.backend.my_authenticated)
        if self.backend.backend_setup and self.backend.my_authenticated:
            #if self.my_library_thread == None:
            #logging.info("lib?")
            #logging.info(self.my_library_thread.is_alive())
            #try:
            await send_events(self) 
            #finally:
            #    loop.close()  
            #try:
            await time_tracking(self, self.my_threads)            #finally:
            #    my_loop.close()   
        await asyncio.sleep(1) 
    
async def setup_queue_to_send_those_changes(self, new_list, old_dict, new_dict):
    await removed_games(self, old_dict, new_dict)    
    await added_games(self, new_list, old_dict, new_dict)                
    await state_changed(self, old_dict, new_dict)
    logging.info("done updates")

async def get_state_changes(old_list, new_list):
    logging.info("get changes")
    logging.info(old_list)
    old_dict = {}
    new_dict = {}
    for current_entry in old_list:
        if ("local_game_state" in list(current_entry.keys()) and "hash_digest" in list(current_entry.keys()) ):
            old_dict[current_entry["hash_digest"]] = current_entry["local_game_state"]
    for current_entry in new_list:
        if ("local_game_state" in list(current_entry.keys()) and "hash_digest" in list(current_entry.keys()) ):
            new_dict[current_entry["hash_digest"]] = current_entry["local_game_state"]
    
    result = {"old":old_dict,"new":new_dict}
    return result

async def shutdown_tasks(self, tasks):
        for task in tasks:
            logging.info("canceling")
            logging.info(task)
            task.cancel()
        
        for task in tasks:
            while not task.done:
                logging.info("waiting for")
                logging.info(tasks)
                await asyncio.sleep(1)

async def update_local_games(self, username, my_game_lister):
    not_run = True
    logging.info("update_local_games")
    logging.info(self.backend.library_run)
    while(self.backend.library_run):
        logging.info("checking for back end library ready")
        logging.info(self.backend.my_authenticated and self.backend.my_imported_owned and self.backend.my_imported_local)
        if self.backend.my_authenticated and self.backend.my_imported_owned and self.backend.my_imported_local:
            #delta is calculated to ensure that we only run expensive operation no more than once a minute
            time_delta_minutes = await time_delta_calc_minutes(self.backend.last_update)
            logging.info("delta")
            logging.info(time_delta_minutes)
            logging.info("not run?")
            logging.info(not_run)
            #TODO could be more specific about rescans
            logging.info("update list not pending?")
            logging.info(self.backend.my_queue_folder_awaiting_scan.empty())
            logging.info("I am not updating?")
            logging.info(self.backend.not_updating_list_scan)
            logging.info("lets go in here for a scan?")
            logging.info(not_run)
            logging.info(not self.backend.my_queue_folder_awaiting_scan.empty() and self.backend.not_updating_list_scan and time_delta_minutes>1)
            logging.info(not_run or (not self.backend.my_queue_folder_awaiting_scan.empty() and self.backend.not_updating_list_scan and time_delta_minutes>1))
            if (not_run or (not self.backend.my_queue_folder_awaiting_scan.empty() and self.backend.not_updating_list_scan and time_delta_minutes>1)):
                logging.info("Starting a full scan")
                self.backend.not_updating_list_scan = False
                while not self.backend.my_queue_folder_awaiting_scan.empty(): 
                    #TODO can limit to these
                    logging.info(self.backend.my_queue_folder_awaiting_scan.get())
                if not_run:
                    logging.info("setting up folder listeners")
                    await my_game_lister.setup_folder_listeners(self.backend.my_queue_folder_awaiting_scan)
                not_run = False
                self.backend.last_update = datetime.now()
                logging.info("get local updates")
                new_local_games_list = await my_game_lister.list_all_recursively(username)
                logging.info("Got new List")
                await prepare_to_send_my_updates(self, new_local_games_list, self.backend.local_game_cache)
                self.backend.not_updating_list_scan = True
                
        logging.info("sleepy")
        await asyncio.sleep(10)
    #tasks = [t for t in asyncio.all_tasks() if t is not
    #         asyncio.current_task()]
    #for task in tasks:
    #    logging.info("canceling")
    #    task.cancel()
    #for task in tasks:
    #        while not task.done:
    #            logging.info("waiting for")
    #            logging.info(tasks)
    logging.info("bye")

def run_my_selected_game_here(execution_command):
    my_command = os.system(execution_command)
    return my_command

async def get_exe_command(game_id,local_game_cache):
    my_game_to_launch={}
    for current_game_checking in local_game_cache:
        my_hash = escapejson(current_game_checking["hash_digest"])
        if (my_hash == game_id):
            my_game_to_launch =  current_game_checking
            break      
    logging.info(my_game_to_launch)
    execution_command = ""
    if "execution" in my_game_to_launch.keys():
        my_replaced_game_to_launch = my_game_to_launch["execution"]
        my_replaced_game_to_launch = my_replaced_game_to_launch.replace("%ROM_RAW%", my_game_to_launch["filename"])
        my_replaced_game_to_launch = my_replaced_game_to_launch.replace("%ROM_DIR%", my_game_to_launch["path"])
        if None == my_game_to_launch["game_filename"]:
            logging.error("Invalid game_filename")
            logging.error(my_game_to_launch)
        my_replaced_game_to_launch = my_replaced_game_to_launch.replace("%ROM_NAME%", my_game_to_launch["game_filename"])
        execution_command="\""+my_replaced_game_to_launch+"\""
        logging.info("starting")
        logging.info(execution_command)
    return execution_command    
    
async def time_delta_calc_minutes(last_update):
    logging.info("time delta calculating")
    current_time = datetime.now()
    logging.info(current_time)
    logging.info(last_update)
    time_delta = (current_time - last_update)
    time_delta_seconds = time_delta.total_seconds()
    return math.ceil(time_delta_seconds/60)    

async def finished_game_run(self, start_time, game_id, local_time_cache):
    logging.info("game finished")
    logging.info(game_id)
    my_delta = await time_delta_calc_minutes(start_time)
    logging.info(my_delta)
    my_cache_update =[]
    placed_game = False
    for current_game in local_time_cache:
        if current_game["hash_digest"] == game_id:
            logging.info("game play time updated")
            logging.info(game_id)
            #update it if it exists in some form
            my_game_update = await created_update(current_game, my_delta, start_time)
            placed_game = True
            my_cache_update.append(my_game_update)
        else:
            #This entry doesn't need an update
            my_cache_update.append(current_game)
    if not placed_game:
        #new entry to be placed
        logging.info("game played for the first time")
        my_game_update = {} 
        my_game_update["run_time_total"] = my_delta
        my_game_update["last_time_played"] = math.floor(start_time.timestamp() )
        my_game_update["hash_digest"] = game_id
        my_cache_update.append(my_game_update)
    await update_cache_time(self, my_cache_update, self.backend.cache_times_filepath)
    my_game_id = escapejson(game_id)
    self.backend.my_queue_update_game_time.put(GameTime(my_game_id, my_game_update["run_time_total"], my_game_update["last_time_played"]))

async def created_update(current_game, my_delta, start_time):
    my_game_update = current_game.copy()
    if "run_time_total" in current_game.keys():
        logging.info("updated play time")
        my_game_update["run_time_total"] = current_game["run_time_total"] + my_delta
    else:
        logging.info("new play time")
        my_game_update["run_time_total"] = my_delta
    my_game_update["last_time_played"] = math.floor(start_time.timestamp() )
    return my_game_update

async def do_auth(self, username):    
    logging.info("Auth request started")
    user_data = {}
    logging.info(username)
    user_data['username'] = username       
    self.store_credentials(user_data)
    self.backend.my_authenticated = True
    return Authentication('importer_user', user_data['username'])

async def update_cache_time(self, my_cache_update, cache_filepath):
    #Potential race condition here probably want to add semaphores on cache writes or refactor
    self.backend.library_lock.acquire()
    try:
        logging.info("locked for time updates")
        self.backend.local_time_cache = my_cache_update
        self.backend.my_game_lister.write_to_cache_file(my_cache_update, cache_filepath)
    finally:
        self.backend.library_lock.release()
        logging.info("lock released for time updates")
    
async def update_cache(self, my_cache_update):
    #Potential race condition here probably want to add semaphores on cache writes or refactor
    self.backend.library_lock.acquire()
    try:
        logging.info("locked for cache updates")
        self.backend.local_game_cache = my_cache_update
        self.backend.my_game_lister.write_to_cache(my_cache_update)
    finally:
        self.backend.library_lock.release()
        logging.info("lock released for cache updates")
