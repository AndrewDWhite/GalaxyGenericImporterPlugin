import sys

from galaxy.api.consts import Platform, LocalGameState
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import Authentication, Game, LocalGame, LicenseInfo, LicenseType, GameLibrarySettings
from typing import Any

import logging
import asyncio
import os
from escapejson import escapejson

#local
from configuration import Default_Config
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
        self.configuration = Default_Config()
        self.local_game_cache = []
        self.create_task_status = None

    # implement methods

    # required
    async def authenticate(self, stored_credentials=None):
        return self.doAuth()

    async def pass_login_credentials(self, step, credentials, cookies):
        return self.doAuth()
    
    def doAuth(self):    
        logging.info("Auth")
        username = ''
        with open(self.configuration.outputUserFile, 'r') as username_file:
            username = username_file.read()

        user_data = {}
        user_data['username'] = username
        self.store_credentials(user_data)
        return Authentication('importer_user', user_data['username'])

    # required
    async def get_owned_games(self):
        logging.info("get owned")
        if self.create_task_status is None:
            logging.info("Creating owned task")
            self.create_task_status = asyncio.create_task(self.update_local_games())
        if not self.create_task_status.done():
            logging.info("awaiting owned task")
            await asyncio.wait({self.create_task_status})
        logging.info("moving on with owned ")
        logging.info(self.create_task_status)
        list_to_galaxy = []
        found_games = self.local_game_cache
        
        for game in found_games:
            this_game=Game(game["hash_digest"], escapejson(game["filename_short"]), None, LicenseInfo(LicenseType.SinglePurchase))
            list_to_galaxy.append(this_game)
        logging.info(len(list_to_galaxy))
        return list_to_galaxy

    # Only placeholders so the feature is recognized
    async def install_game(self, game_id):
        pass

    async def uninstall_game(self, game_id):
        pass
    
    async def get_game_library_settings(self, game_id: str, context: Any)  -> GameLibrarySettings:
        logging.info("Updating library "+game_id)
        my_current_game_selected={}
        if self.create_task_status is None:
            logging.info("Creating update task")
            self.create_task_status = asyncio.create_task(self.update_local_games())
        if not self.create_task_status.done():
            logging.info("awaiting update task")
            await self.create_task_status
        for current_game_checking in self.local_game_cache:
            if (current_game_checking["hash_digest"] == game_id):
                my_current_game_selected =  current_game_checking
                break
        game_tags = [my_current_game_selected["name"]]
        logging.info(my_current_game_selected["name"])
        game_settings = GameLibrarySettings(game_id, game_tags, False)
        return game_settings
    
    def get_state_changes(self, old_list, new_list):
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

    def sendThoseChanges(self, new_list, old_dict,new_dict):
        # removed games
        for my_id in (old_dict.keys() - new_dict.keys()):
            logging.info("removed")
            self.update_local_game_status(LocalGame(my_id, LocalGameState.None_))
        # added games
        for local_game in new_list:
            if ("hash_digest" in local_game) and (local_game["hash_digest"] in (new_dict.keys() - old_dict.keys())):
                logging.info("added")
                #self.remove_game(local_game["hash_digest"])
                self.add_game(Game(local_game["hash_digest"], escapejson(local_game["filename_short"]), None, LicenseInfo(LicenseType.SinglePurchase)))
                self.update_local_game_status(LocalGame(local_game["hash_digest"], LocalGameState.Installed))
                    
        # state changed
        for my_id in new_dict.keys() & old_dict.keys():
            if new_dict[my_id] != old_dict[my_id]:
                logging.info("changed")
                self.update_local_game_status(LocalGame(my_id, new_dict[my_id]))
        logging.info("done updates")    

    def sendMyUpdates(self, new_local_games_list):
        logging.info("sending updates")
        for entry in new_local_games_list:
            if("local_game_state" not in entry):
                entry["local_game_state"]=LocalGameState.Installed

        state_changes = self.get_state_changes(self.local_game_cache, new_local_games_list)
        self.sendThoseChanges(new_local_games_list, state_changes["old"], state_changes["new"])
        self.local_game_cache = new_local_games_list
        #self.update_game(Game(currentGameEntry["hash_digest"], escapejson(currentGameEntry["filename_short"]), None, LicenseInfo(LicenseType.SinglePurchase)))
        
    async def update_local_games(self):
        logging.info("get local updates")
        loop = asyncio.get_running_loop()
        new_local_games_list = await loop.run_in_executor(None, ListGames().list_all_recursively)
        logging.info("Got new List")
        self.sendMyUpdates(new_local_games_list)
        await asyncio.sleep(60)

    async def get_local_games(self):
        logging.info("get local")
        localgames = []
        if self.create_task_status is None:
                self.create_task_status = asyncio.create_task(self.update_local_games())
        if not self.create_task_status.done():
            await asyncio.wait({self.create_task_status})
        logging.info("moving on with local ")
        logging.info(self.create_task_status)
        for local_game in self.local_game_cache :
            localgames.append(LocalGame(local_game["hash_digest"], LocalGameState.Installed))
        logging.info(len(localgames))
        return localgames
    
    def tick(self):
        if self.create_task_status is None or self.create_task_status.done():
            self.create_task_status = asyncio.create_task(self.update_local_games())    

    def runMySelectedGameHere(self, execution_command):
        os.system(execution_command)

    def getExeCommand(self, game_id,local_game_cache):
        my_game_to_launch={}
        for current_game_checking in local_game_cache:
            if (current_game_checking["hash_digest"] == game_id):
                my_game_to_launch =  current_game_checking
                break      
        print (my_game_to_launch)
        execution_command = ""
        if "execution" in my_game_to_launch.keys():
            execution_command="\""+my_game_to_launch["execution"].replace("%ROM_RAW%", my_game_to_launch["filename"]).replace("%ROM_DIR%", my_game_to_launch["path"]).replace("%ROM_NAME%", my_game_to_launch["gamename"])+"\""
            logging.info("starting")
            logging.info(execution_command)
        return execution_command

    async def launch_game(self, game_id):
        logging.info("launch")
        execution_command = self.getExeCommand(game_id, self.local_game_cache)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.runMySelectedGameHere,execution_command)
        logging.info("returned")            
    
def main():
    create_and_run_plugin(GenericEmulatorPlugin, sys.argv)

# run plugin event loop
if __name__ == "__main__":
    main()