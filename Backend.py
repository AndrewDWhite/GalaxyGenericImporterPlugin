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
import time
import queue

class Backend():
        
    def __init__(self, configuration):
        self.last_update = datetime.now()
        self.my_imported_owned = False
        self.my_imported_local = False
        self.my_game_lister =  ListGames()
        self.local_game_cache = self.my_game_lister.read_from_cache()
        self.cache_times_filepath = self.my_game_lister.cache_filepath+"-times"
        self.local_time_cache = []
        if self.my_game_lister.cache_exists_file(self.cache_times_filepath):
            self.local_time_cache = self.my_game_lister.read_from_cache_filename(self.cache_times_filepath)
        self.library_lock = threading.Lock()
        self.library_run = True
        self.my_authenticated = False
        self.my_queue_update_local_game_status = queue.Queue()
        self.my_queue_add_game = queue.Queue()
        self.my_queue_update_game_time = queue.Queue()
        self.not_updating = True
        logging.info("backend started up")
        
def shutdown_library(self):
    logging.info("Library update in progress?")
    self.backend.library_run= False
    self.my_library_thread.join() 

def time_tracking(self, my_threads):
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
            finished_game_run(self, datetime.fromisoformat(my_dictionary_values["time"]),my_dictionary_values["id"], self.backend.local_time_cache)
            my_threads_to_remove.append(my_current_thread)
    for my_thread_to_remove in my_threads_to_remove:
        logging.info("thread removed")
        my_threads.remove(my_thread_to_remove)
        
def create_game(game):
    return Game(escapejson(game["hash_digest"]), escapejson(game["game_name"]), None, LicenseInfo(LicenseType.SinglePurchase))

def prepare_to_send_my_updates(self, new_local_games_list, local_game_cache):
    logging.info("sending updates")
    for entry in new_local_games_list:
        if("local_game_state" not in entry):
            entry["local_game_state"]=LocalGameState.Installed
    state_changes = get_state_changes(local_game_cache, new_local_games_list)
    setup_queue_to_send_those_changes(self, new_local_games_list, state_changes["old"], state_changes["new"])
    update_cache(self, new_local_games_list)

#Will cause issues it not called from initial thread
def send_events(self):
    logging.info("sending events to galaxy")
    logging.info("my_queue_add_game")
    logging.info(self.backend.my_queue_add_game.empty())
    while not self.backend.my_queue_add_game.empty():
        my_game_sending = self.backend.my_queue_add_game.get()
        logging.info(my_game_sending)
        self.add_game(my_game_sending)
    
    logging.info("my_queue_update_local_game_status")
    logging.info(self.backend.my_queue_update_local_game_status.empty())    
    while not self.backend.my_queue_update_local_game_status.empty():
        my_game_sending = self.backend.my_queue_update_local_game_status.get()
        logging.info(my_game_sending)
        self.update_local_game_status(my_game_sending)
  
    logging.info("my_queue_update_game_time")
    logging.info(self.backend.my_queue_update_game_time.empty())    
    while not self.backend.my_queue_update_game_time.empty():    
        my_game_sending = self.backend.my_queue_update_game_time.get()
        logging.info(my_game_sending)
        self.update_game_time(my_game_sending)

def removed_games(self, old_dict, new_dict):
    # removed games
    for my_id in (old_dict.keys() - new_dict.keys()):
        logging.info("removed")
        self.backend.my_queue_update_local_game_status.put(LocalGame(my_id, LocalGameState.None_))

def added_games(self, new_list, old_dict, new_dict):
    # added games
    for local_game in new_list:
        if ("hash_digest" in local_game) and (local_game["hash_digest"] in (new_dict.keys() - old_dict.keys())):
            logging.info("added")
            self.backend.my_queue_add_game.put(create_game(local_game))
            self.backend.my_queue_update_local_game_status.put(LocalGame(local_game["hash_digest"], LocalGameState.Installed))

def state_changed(self, old_dict, new_dict):
    # state changed
    for my_id in new_dict.keys() & old_dict.keys():
        if new_dict[my_id] != old_dict[my_id]:
            logging.info("changed")
            self.backend.my_queue_update_local_game_status.put(LocalGame(my_id, new_dict[my_id]))
    
def setup_queue_to_send_those_changes(self, new_list, old_dict, new_dict):
    removed_games(self, old_dict, new_dict)    
    added_games(self, new_list, old_dict, new_dict)                
    state_changed(self, old_dict, new_dict)
    logging.info("done updates")

def get_state_changes(old_list, new_list):
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

def update_local_games(self, username, my_game_lister):
    not_run = True
    logging.info("update_local_games")
    logging.info(self.backend.library_run)
    while(self.backend.library_run):
        if self.backend.my_authenticated and self.backend.my_imported_owned and self.backend.my_imported_local:
            #delta is calculated to ensure that we only run expensive operation no more than once a minute
            time_delta_minutes = time_delta_calc_minutes(self.backend.last_update)
            #logging.info("delta")
            #logging.info(time_delta_minutes)
            #logging.info("not run?")
            #logging.info(not_run)
            if not_run or (my_game_lister.update_list_pending and self.not_updating and time_delta_minutes>1):
                self.not_updating = False
                my_game_lister.update_list_pending = False
                if not_run:
                    my_game_lister.setup_folder_listeners(self)
                not_run = False
                self.backend.last_update = datetime.now()
                logging.info("get local updates")
                new_local_games_list = my_game_lister.list_all_recursively(username)
                logging.info("Got new List")
                prepare_to_send_my_updates(self, new_local_games_list, self.backend.local_game_cache)
                self.not_updating = True
                
        logging.info("sleepy")
        time.sleep(10)
    logging.info("bye")

def run_my_selected_game_here(execution_command):
    return os.system(execution_command)

def get_exe_command(game_id,local_game_cache):
    my_game_to_launch={}
    for current_game_checking in local_game_cache:
        if (escapejson(current_game_checking["hash_digest"]) == game_id):
            my_game_to_launch =  current_game_checking
            break      
    logging.info(my_game_to_launch)
    execution_command = ""
    if "execution" in my_game_to_launch.keys():
        execution_command="\""+my_game_to_launch["execution"].replace("%ROM_RAW%", my_game_to_launch["filename"]).replace("%ROM_DIR%", my_game_to_launch["path"]).replace("%ROM_NAME%", my_game_to_launch["game_filename"])+"\""
        logging.info("starting")
        logging.info(execution_command)
    return execution_command    
    
def time_delta_calc_minutes(last_update):
    current_time = datetime.now()
    logging.info(current_time)
    logging.info(last_update)
    time_delta = (current_time - last_update)
    time_delta_seconds = time_delta.total_seconds()
    return math.ceil(time_delta_seconds/60)    

def finished_game_run(self, start_time, game_id, local_time_cache):
    logging.info("game finished")
    logging.info(game_id)
    my_delta = time_delta_calc_minutes(start_time)
    logging.info(my_delta)
    my_cache_update =[]
    placed_game = False
    for current_game in local_time_cache:
        if current_game["hash_digest"] == game_id:
            logging.info("game play time updated")
            logging.info(game_id)
            #update it if it exists in some form
            my_game_update = created_update(current_game, my_delta, start_time)
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
    update_cache_time(self, my_cache_update, self.backend.cache_times_filepath)
    self.backend.my_queue_update_game_time.put(GameTime(escapejson(game_id), my_game_update["run_time_total"], my_game_update["last_time_played"]))

def created_update(current_game, my_delta, start_time):
    my_game_update = current_game.copy()
    if "run_time_total" in current_game.keys():
        logging.info("updated play time")
        my_game_update["run_time_total"] = current_game["run_time_total"] + my_delta
    else:
        logging.info("new play time")
        my_game_update["run_time_total"] = my_delta
    my_game_update["last_time_played"] = math.floor(start_time.timestamp() )
    return my_game_update

def do_auth(self, username):    
    logging.info("Auth")
    user_data = {}
    logging.info(username)
    user_data['username'] = username       
    self.store_credentials(user_data)
    self.backend.my_authenticated = True
    return Authentication('importer_user', user_data['username'])

def update_cache_time(self, my_cache_update, cache_filepath):
    #Potential race condition here probably want to add semaphores on cache writes or refactor
    self.backend.library_lock.acquire()
    try:
        logging.info("locked")
        self.backend.local_time_cache = my_cache_update
        self.backend.my_game_lister.write_to_cache_file(my_cache_update, cache_filepath)
    finally:
        self.backend.library_lock.release()
    
def update_cache(self, my_cache_update):
    #Potential race condition here probably want to add semaphores on cache writes or refactor
    self.backend.library_lock.acquire()
    try:
        logging.info("locked")
        self.backend.local_game_cache = my_cache_update
        self.backend.my_game_lister.write_to_cache(my_cache_update)
    finally:
        self.backend.library_lock.release()
