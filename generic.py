import sys

from galaxy.api.consts import Platform, LocalGameState
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import Authentication, Game, LocalGame, LicenseInfo, LicenseType, GameLibrarySettings
from typing import Any

import logging
import os
from escapejson import escapejson
from datetime import datetime
import functools
import math

#local
from configuration import DefaultConfig
from ListGames import ListGames

class GenericEmulatorPlugin(Plugin):
    def __init__(self, reader, writer, token):
        super().__init__(
            Platform.Test,  # choose platform from available list
            "0.1",  # version
            reader,
            writer,
            token
        )
        self.configuration = DefaultConfig()
        self.create_task_status = None
        self.my_game_lister =  ListGames()        
        self.local_game_cache = self.my_game_lister.read_from_cache()
        self.last_update = datetime.now()
        self.my_authenticated = False
        self.my_imported_owned = False
        self.my_imported_local = False

    # required api interface to authenticate the user with the platform
    async def authenticate(self, stored_credentials=None):
        logging.info("authenticate called")
        return do_auth(self)

    # required api interface
    async def pass_login_credentials(self, step, credentials, cookies):
        logging.info("pass_login_credentials called")
        return do_auth(self)
    
    # required api interface to return the owned games
    async def get_owned_games(self):
        logging.info("get owned")
        #call function to update
        if self.create_task_status is None:
            logging.info("Creating owned task")
            self.create_task_status = self.create_task(update_local_games(self), "Creating owned task")
            await self.create_task_status
        else:
            if not self.create_task_status.done():
                await self.create_task_status
        logging.info("moving on with owned ")
        logging.info(self.create_task_status)
        list_to_galaxy = []
        found_games = self.local_game_cache
        
        for game in found_games:
            this_game=create_game(game)
            list_to_galaxy.append(this_game)
        logging.info(len(list_to_galaxy))
        self.my_imported_owned = True
        return list_to_galaxy

    # api interface to install games
    # Only placeholder so the get_local_games feature is recognized
    async def install_game(self, game_id):
        logging.info("install called")
        logging.info(game_id)

    # api interface to uninstall games
    # Only placeholder so the get_local_games feature is recognized
    async def uninstall_game(self, game_id):
        logging.info("uninstall called")
        logging.info(game_id)
    
    # api interface to update game library data with tags
    # appears that get_owned_games will always run first 
    async def get_game_library_settings(self, game_id: str, context: Any)  -> GameLibrarySettings:
        logging.info("Updating library "+game_id)
        my_current_game_selected={}
        #call function to update
        if self.create_task_status is None:
            logging.info("Creating update task")
            self.create_task_status = self.create_task(update_local_games(self), "Creating update task")
        for current_game_checking in self.local_game_cache:
            if (escapejson(current_game_checking["hash_digest"]) == game_id):
                my_current_game_selected =  current_game_checking
                break
        game_tags = my_current_game_selected["tags"]
        logging.info(game_tags)
        game_settings = GameLibrarySettings(game_id, game_tags, False)
        return game_settings

    # api interface to return locally installed games
    async def get_local_games(self):
        logging.info("get local")
        localgames = []
        #call function to update 
        if self.create_task_status is None:
                self.create_task_status = self.create_task(update_local_games(self), "get local")
                await self.create_task_status
        else:
            if not self.create_task_status.done():
                await self.create_task_status
        logging.info("moving on with local ")
        logging.info(self.create_task_status)
        for local_game in self.local_game_cache :
            localgames.append(LocalGame(local_game["hash_digest"], LocalGameState.Installed))
        logging.info(len(localgames))
        self.my_imported_local = True
        return localgames
    
    # api interface to periodically run processes such as rescanning for library changes
    def tick(self):
        if self.my_authenticated and self.my_imported_owned and self.my_imported_local:
            time_delta_minutes = time_delta_calc_minutes(self.last_update)
            #delta is calculated to ensure that we only run expensive operation no more than once a minute
            
            if self.create_task_status is None or (self.create_task_status.done() and time_delta_minutes>1):
                self.last_update = datetime.now()
                self.create_task_status = self.create_task(update_local_games(self), "tick update")    

    # api interface shutdown nicely
    def shutdown(self):
        logging.info("shutdown called")

    # api interface to startup game
    # requires get_local_games to have listed the game
    async def launch_game(self, game_id):
        logging.info("launch")
        execution_command = get_exe_command(game_id, self.local_game_cache)
        my_current_time = datetime.now()
        my_coroutine = run_my_selected_game_here(execution_command)
        my_coroutine_task = self.create_task(my_coroutine, "starting game")
        my_coroutine_task.add_done_callback(functools.partial(finished_game_run, self, my_current_time, game_id))       

def create_game(game):
    return Game(escapejson(game["hash_digest"]), escapejson(game["game_name"]), None, LicenseInfo(LicenseType.SinglePurchase))

def send_my_updates(self, new_local_games_list):
    logging.info("sending updates")
    for entry in new_local_games_list:
        if("local_game_state" not in entry):
            entry["local_game_state"]=LocalGameState.Installed

    state_changes = get_state_changes(self.local_game_cache, new_local_games_list)
    send_those_changes(self, new_local_games_list, state_changes["old"], state_changes["new"])
    self.local_game_cache = new_local_games_list
    #self.update_game(Game(currentGameEntry["hash_digest"], escapejson(currentGameEntry["filename_short"]), None, LicenseInfo(LicenseType.SinglePurchase)))


def send_those_changes(self, new_list, old_dict,new_dict):
    # removed games
    for my_id in (old_dict.keys() - new_dict.keys()):
        logging.info("removed")
        self.update_local_game_status(LocalGame(my_id, LocalGameState.None_))
    # added games
    for local_game in new_list:
        if ("hash_digest" in local_game) and (local_game["hash_digest"] in (new_dict.keys() - old_dict.keys())):
            logging.info("added")
            #self.remove_game(local_game["hash_digest"])
            self.add_game(create_game(local_game))
            self.update_local_game_status(LocalGame(local_game["hash_digest"], LocalGameState.Installed))
                
    # state changed
    for my_id in new_dict.keys() & old_dict.keys():
        if new_dict[my_id] != old_dict[my_id]:
            logging.info("changed")
            self.update_local_game_status(LocalGame(my_id, new_dict[my_id]))
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

async def update_local_games(self):
    logging.info("get local updates")
    new_local_games_list = self.my_game_lister.list_all_recursively(self.configuration.my_user_to_gog)
    logging.info("Got new List")
    send_my_updates(self, new_local_games_list)
    self.my_game_lister.write_to_cache(new_local_games_list)

async def run_my_selected_game_here(execution_command):
    os.system(execution_command)

def get_exe_command(game_id,local_game_cache):
    my_game_to_launch={}
    for current_game_checking in local_game_cache:
        if (current_game_checking["hash_digest"] == game_id):
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

def finished_game_run(self, start_time, game_id, future):
    logging.info("game finished")
    logging.info(game_id)
    my_delta = time_delta_calc_minutes(start_time)
    logging.info(my_delta)
    #TODO implement logging of time
    return self

def do_auth(self):    
    logging.info("Auth")
    user_data = {}
    username = self.configuration.my_user_to_gog
    logging.info(username)
    user_data['username'] = username       
    self.store_credentials(user_data)
    self.my_authenticated = True
    return Authentication('importer_user', user_data['username'])

    
def main():
    create_and_run_plugin(GenericEmulatorPlugin, sys.argv)

# run plugin event loop
if __name__ == "__main__":
    main()