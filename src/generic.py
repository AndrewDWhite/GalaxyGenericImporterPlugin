import sys

from galaxy.api.consts import Platform
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import LocalGame, GameLibrarySettings, GameTime
from typing import Any

import logging
from escapejson import escapejson
import json
from datetime import datetime
import threading
import asyncio

#local
from configuration import DefaultConfig
from Backend import Backend, do_auth, shutdown_library, tick_async, library_thread
from GalaxyPluginUtils import create_game
from TaskManagementUtil import shutdown_tasks
from ExecutionUtil import run_my_selected_game_here
from CacheDataManipulation import  get_exe_command

class GenericEmulatorPlugin(Plugin):
    def __init__(self, reader, writer, token):
        self.configuration = DefaultConfig()
        
        super().__init__(
            Platform(self.configuration.my_platform_to_gog), # choose platform from available list
            "0.1",  # version
            reader,
            writer,
            token
        )         
        self.backend = Backend()
        self.my_library_thread = None
        self.my_library_started = False
        self.my_threads = []    
        self.my_tasks = []
        self.started_async_tick = False
        self.keep_ticking = True 
        if (self.configuration.minimize_logging):
            logging.getLogger().setLevel(logging.WARNING)
        else:
            logging.getLogger().setLevel(logging.DEBUG)

    #Wait for the backend to setup to help reduce the amount of issues with galaxy and race conditions
    def handshake_complete(self):
        logging.info("Handshake complete")
        self.backend.my_handshook=True
        if not self.backend.backend_setup and self.configuration.force_batch_mode_initial_seed:
            self.backend.setup(self.configuration)

    # required api interface to authenticate the user with the platform
    async def authenticate(self, stored_credentials=None):
        logging.debug("authenticate called")
        my_auth = await do_auth(self, self.configuration.my_user_to_gog)
        return my_auth

    # required api interface
    async def pass_login_credentials(self, step, credentials, cookies):
        logging.debug("pass_login_credentials called")
        my_auth = await do_auth(self, self.configuration.my_user_to_gog)
        return my_auth
    
    # required api interface to return the owned games
    async def get_owned_games(self):
        logging.debug("get local games will wait for library to setup if necessary")
        if not self.backend.backend_setup:
            await self.backend.setup(self.configuration)
        logging.debug("get owned")
        list_to_galaxy = []
        found_games = self.backend.local_game_cache
        
        for game in found_games:
            this_game=await create_game(game)
            list_to_galaxy.append(this_game)
        logging.debug(len(list_to_galaxy))
        self.backend.my_imported_owned = True
        return list_to_galaxy

    # api interface to install games
    # Only placeholder so the get_local_games feature is recognized
    async def install_game(self, game_id):
        logging.debug("install called")
        logging.debug(game_id)

    async def get_game_time(self, game_id, context):
        logging.debug("getting play time")
        logging.debug(game_id)
        for current_game in self.backend.local_time_cache:
            if escapejson(current_game["hash_digest"]) == game_id:
                logging.debug(current_game["last_time_played"])
                logging.debug(current_game["run_time_total"])
                return GameTime(game_id, current_game["run_time_total"], current_game["last_time_played"])
        #not in cache so never played
        logging.debug("never played")
        return GameTime(game_id, 0, None)

    # api interface to uninstall games
    # Only placeholder so the get_local_games feature is recognized
    async def uninstall_game(self, game_id):
        logging.debug("uninstall called")
        logging.debug(game_id)
    
    # api interface to update game library data with tags
    # assumes that library has already been imported
    async def get_game_library_settings(self, game_id: str, context: Any)  -> GameLibrarySettings:
        logging.debug("Updating library "+game_id)
        my_current_game_selected={}
        #call function to update
        for current_game_checking in self.backend.local_game_cache:
            my_escaped_id = escapejson(current_game_checking["hash_digest"])
            if (my_escaped_id == game_id):
                my_current_game_selected =  current_game_checking
                break
        game_tags = my_current_game_selected["tags"]
        logging.debug(game_tags)
        game_settings = GameLibrarySettings(game_id, game_tags, False)
        return game_settings

    # api interface to return locally installed games
    # appears that get_owned_games will always run first
    async def get_local_games(self):
        logging.debug("get local games will wait for library to setup if necessary")
        if not self.backend.backend_setup:
            await self.backend.setup(self.configuration)

        logging.debug("get local")
        localgames = []
        for local_game in self.backend.local_game_cache :
            if local_game["gameShouldBeInstalled"]:
                localgames.append(LocalGame(local_game["hash_digest"], local_game["local_game_state"]))
            else:
                logging.debug("Only Owned:")
                logging.debug(local_game)
        logging.debug(len(localgames))
        self.backend.my_imported_local = True
        return localgames
    
    # mod of api interface to periodically run processes such as rescanning for library changes
    def tick(self):
        if not self.started_async_tick:
            logging.debug("Setup ticking")
            self.started_async_tick = True
            asyncio.get_event_loop()
            my_task = asyncio.create_task(tick_async(self) )
            self.my_tasks.append(my_task)
            
            
            logging.debug("tick setup will initialize backend setup if necessary")
            if not self.backend.backend_setup:
                logging.debug("Backend setup was necessary")
                my_task_update = asyncio.create_task(self.backend.setup(self.configuration) )
                self.my_tasks.append(my_task_update)
                
            else:
                logging.debug("Backend was setup already")
            
            logging.debug("starting library thread up for the first time")
            self.my_library_thread = threading.Thread(target=library_thread, args=(self, ) )
            self.my_library_thread.daemon = True
            self.my_library_thread.start()    
            
            #Lets just send the game data once just incase
            my_task_owned = asyncio.create_task(self.get_owned_games())
            self.my_tasks.append(my_task_owned)
            my_task_local = asyncio.create_task(self.get_local_games())
            self.my_tasks.append(my_task_local)
            logging.debug("end setup ticking")

    # api interface shutdown nicely
    async def shutdown(self):
        logging.debug("shutdown called")
        self.keep_ticking = False
        
        await shutdown_tasks(self, self.my_tasks)
        
        await shutdown_library(self)
        
        tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]
        for my_task in tasks:
            logging.info("still running")
            logging.info(my_task)
        
        #loop = asyncio.get_event_loop()
        #loop.close()
        #await asyncio.sleep(3)
        logging.debug("all done shutdown")

    # api interface to startup game
    # requires get_local_games to have listed the game
    async def launch_game(self, game_id):
        logging.debug("launch program")
        execution_command = await get_exe_command(game_id, self.backend.local_game_cache)
        my_current_time = datetime.now()
        logging.debug(execution_command)
        my_thread= threading.Thread(target=run_my_selected_game_here, args=(execution_command,logging,))
        self.my_threads.append(my_thread)
        my_thread.name = json.dumps({"time":my_current_time.isoformat(), "id":game_id})
        logging.debug(my_thread.name)
        my_thread.daemon = True
        my_thread.start()
        #We don't hang the closing of the plugin for this to stop
  
def main():
    create_and_run_plugin(GenericEmulatorPlugin, sys.argv)

# run plugin event loop
if __name__ == "__main__":
    main()