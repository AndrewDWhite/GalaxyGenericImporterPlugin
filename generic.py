import sys

from galaxy.api.consts import Platform, LocalGameState
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import LocalGame, GameLibrarySettings, GameTime
from typing import Any

import logging
from escapejson import escapejson
import json
from datetime import datetime
import threading

#local
from configuration import DefaultConfig
from Backend import Backend, time_tracking, create_game, run_my_selected_game_here, get_exe_command, do_auth, shutdown_library, send_events, update_local_games

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
        self.backend = Backend(self.configuration)        
        self.my_threads = []
        self.my_library_thread = threading.Thread(target=update_local_games, args=(self, self.configuration.my_user_to_gog, self.backend.my_game_lister,))
        self.my_library_thread.start()
        

    # required api interface to authenticate the user with the platform
    async def authenticate(self, stored_credentials=None):
        logging.info("authenticate called")
        return do_auth(self, self.configuration.my_user_to_gog)

    # required api interface
    async def pass_login_credentials(self, step, credentials, cookies):
        logging.info("pass_login_credentials called")
        return do_auth(self, self.configuration.my_user_to_gog)
    
    # required api interface to return the owned games
    async def get_owned_games(self):
        logging.info("get owned")
        list_to_galaxy = []
        found_games = self.backend.local_game_cache
        
        for game in found_games:
            this_game=create_game(game)
            list_to_galaxy.append(this_game)
        logging.info(len(list_to_galaxy))
        self.backend.my_imported_owned = True
        return list_to_galaxy

    # api interface to install games
    # Only placeholder so the get_local_games feature is recognized
    async def install_game(self, game_id):
        logging.info("install called")
        logging.info(game_id)

    async def get_game_time(self, game_id, context):
        logging.info("getting play time")
        logging.info(game_id)
        for current_game in self.backend.local_time_cache:
            if escapejson(current_game["hash_digest"]) == game_id:
                logging.info(current_game["last_time_played"])
                logging.info(current_game["run_time_total"])
                return GameTime(game_id, current_game["run_time_total"], current_game["last_time_played"])
        #not in cache so never played
        logging.info("never played")
        return GameTime(game_id, 0, None)

    # api interface to uninstall games
    # Only placeholder so the get_local_games feature is recognized
    async def uninstall_game(self, game_id):
        logging.info("uninstall called")
        logging.info(game_id)
    
    # api interface to update game library data with tags
    # assumes that library has already been imported
    async def get_game_library_settings(self, game_id: str, context: Any)  -> GameLibrarySettings:
        logging.info("Updating library "+game_id)
        my_current_game_selected={}
        #call function to update
        for current_game_checking in self.backend.local_game_cache:
            if (escapejson(current_game_checking["hash_digest"]) == game_id):
                my_current_game_selected =  current_game_checking
                break
        game_tags = my_current_game_selected["tags"]
        logging.info(game_tags)
        game_settings = GameLibrarySettings(game_id, game_tags, False)
        return game_settings

    # api interface to return locally installed games
    # appears that get_owned_games will always run first
    async def get_local_games(self):
        logging.info("get local")
        localgames = []
        for local_game in self.backend.local_game_cache :
            localgames.append(LocalGame(local_game["hash_digest"], LocalGameState.Installed))
        logging.info(len(localgames))
        self.backend.my_imported_local = True
        return localgames
    
    # api interface to periodically run processes such as rescanning for library changes
    def tick(self):   
        logging.info("lib?")
        logging.info(self.my_library_thread.is_alive())
        send_events(self)         
        time_tracking(self, self.my_threads)

    # api interface shutdown nicely
    async def shutdown(self):
        logging.info("shutdown called")
        
        shutdown_library(self)

        logging.info("all done shutdown")

    # api interface to startup game
    # requires get_local_games to have listed the game
    async def launch_game(self, game_id):
        logging.info("launch")
        execution_command = get_exe_command(game_id, self.backend.local_game_cache)
        my_current_time = datetime.now()
        logging.info(execution_command)
        my_thread= threading.Thread(target=run_my_selected_game_here, args=(execution_command,))
        self.my_threads.append(my_thread)
        my_thread.name = json.dumps({"time":my_current_time.isoformat(), "id":game_id})
        logging.info(my_thread.name)
        my_thread.start()
  
def main():
    create_and_run_plugin(GenericEmulatorPlugin, sys.argv)

# run plugin event loop
if __name__ == "__main__":
    main()