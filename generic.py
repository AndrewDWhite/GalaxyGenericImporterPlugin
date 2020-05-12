import sys

from galaxy.api.consts import Platform, LocalGameState
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import Authentication, Game, LocalGame, LicenseInfo, LicenseType, GameLibrarySettings
from typing import Any

import subprocess
import logging
import asyncio
import os
from escapejson import escapejson

#local
from configuration import Default_Config
from list_games import List_Games

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
                self.create_task_status = self.create_task(self.update_local_games(), 'Update local games')
        if not self.create_task_status.done():
            await self.create_task_status
        logging.info("moving on with owned")
        listToGalaxy = []
        found_games = self.local_game_cache
        
        #with open(self.configuration.outputFile, 'w') as filehandle:
        for game in found_games:
            #filehandle.write('%s\n' % game)
            #self.update_local_game_status(LocalGame(game["hash_digest"], LocalGameState.Installed))
            thisGame=Game(game["hash_digest"], escapejson(game["filename_short"]), None, LicenseInfo(LicenseType.SinglePurchase))
            listToGalaxy.append(thisGame)
        
        return listToGalaxy

    # Only placeholders so the feature is recognized
    async def install_game(self, game_id):
        pass

    async def uninstall_game(self, game_id):
        pass
    
    async def get_game_library_settings(self, game_id: str, context: Any)  -> GameLibrarySettings:
        logging.info("Updating library "+game_id)
        myCurrentGameSelected={}
        if self.create_task_status is None:
                self.create_task_status = self.create_task(self.update_local_games(), 'Update local games')
        if not self.create_task_status.done():
            await self.create_task_status
        for currentGameChecking in self.local_game_cache:
            if (currentGameChecking["hash_digest"] == game_id):
                myCurrentGameSelected =  currentGameChecking
                break
        gameTags = [myCurrentGameSelected["name"]]
        gameSettings = GameLibrarySettings(game_id, gameTags, False)
        return gameSettings
    
    def get_state_changes(self, old_list, new_list):
        logging.info("get changes")
        logging.info(old_list)
        old_dict = {}
        new_dict = {}
        for currentEntry in old_list:
            if ("local_game_state" in list(currentEntry.keys()) and "hash_digest" in list(currentEntry.keys()) ):
                old_dict[currentEntry["hash_digest"]] = currentEntry["local_game_state"]
        for currentEntry in new_list:
            #print("local_game_state" in list(currentEntry.keys()))
            if ("local_game_state" in list(currentEntry.keys()) and "hash_digest" in list(currentEntry.keys()) ):
                new_dict[currentEntry["hash_digest"]] = currentEntry["local_game_state"]
        
        result = {"old":old_dict,"new":new_dict}
        return result

    def sendThoseChanges(self, new_list, old_dict,new_dict):
        # removed games
        for myId in (old_dict.keys() - new_dict.keys()):
            logging.info("removed")
            self.update_local_game_status(LocalGame(myId, LocalGameState.None_))
        # added games
        for local_game in new_list:
            #print(local_game)
            #print(local_game["hash_digest"])
            #print("hash_digest" in local_game)
            #print((new_dict.keys() - old_dict.keys()))
            #print(new_dict.keys())
            if ("hash_digest" in local_game) and (local_game["hash_digest"] in (new_dict.keys() - old_dict.keys())):
                logging.info("added")
                #self.remove_game(local_game["hash_digest"])
                self.add_game(Game(local_game["hash_digest"], escapejson(local_game["filename_short"]), None, LicenseInfo(LicenseType.SinglePurchase)))
                self.update_local_game_status(LocalGame(local_game["hash_digest"], LocalGameState.Installed))
                    
        # state changed
        for myId in new_dict.keys() & old_dict.keys():
            if new_dict[myId] != old_dict[myId]:
                logging.info("changed")
                self.update_local_game_status(LocalGame(myId, new_dict[myId]))
        #return result
        logging.info("done updates")    

    def sendMyUpdates(self, new_local_games_list):
        logging.info("sending updates")
        for entry in new_local_games_list:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed

        #notify_list = 
        stateChanges = self.get_state_changes(self.local_game_cache, new_local_games_list)
        self.sendThoseChanges(new_local_games_list, stateChanges["old"], stateChanges["new"])
        self.local_game_cache = new_local_games_list
        #self.update_game(Game(currentGameEntry["hash_digest"], escapejson(currentGameEntry["filename_short"]), None, LicenseInfo(LicenseType.SinglePurchase)))
        #await asyncio.sleep(60)

    async def update_local_games(self):
        logging.info("get local updates")
        loop = asyncio.get_running_loop()
        new_local_games_list = await loop.run_in_executor(None, List_Games().listAllRecursively)
        logging.info("Got new List")
        self.sendMyUpdates(new_local_games_list)
        #for local_game_notify in notify_list:
        #    logging.info("sending update")
        #    logging.info(local_game_notify)
        #    if ("game" in local_game_notify):
        #        self.add_game(local_game_notify["game"])
        #    self.update_local_game_status(local_game_notify["local"])
        await asyncio.sleep(60)

    async def get_local_games(self):
        logging.info("get local")
        localgames = []
        if self.create_task_status is None:
                self.create_task_status = self.create_task(self.update_local_games(), 'Update local games')
        if not self.create_task_status.done():
            await self.create_task_status
        logging.info("moving on with local")
        for local_game in self.local_game_cache :
            localgames.append(LocalGame(local_game["hash_digest"], LocalGameState.Installed))
        return localgames
    
    def tick(self):
        #self.local_game_cache = {currentEntry.game_id: 0 for currentEntry in self.local_games_list()}
        #self.create_task(self.update_games(), 'Update games')    
        if self.create_task_status is None or self.create_task_status.done():
            self.create_task_status = self.create_task(self.update_local_games(), 'Update local games')    

    def runMySelectedGameHere(self, executionCommand):
        os.system(executionCommand)

    def getExeCommand(self, game_id,local_game_cache):
        myGameToLaunch={}
        for currentGameChecking in local_game_cache:
            if (currentGameChecking["hash_digest"] == game_id):
                myGameToLaunch =  currentGameChecking
                break      
        print (myGameToLaunch)
        executionCommand = ""
        if "execution" in myGameToLaunch.keys():
            executionCommand="\""+myGameToLaunch["execution"].replace("%ROM_RAW%", myGameToLaunch["filename"])+"\""
            logging.info("starting")
            logging.info(executionCommand)
        return executionCommand

    async def launch_game(self, game_id):
        logging.info("launch")
        # define an empty list
        #myPreLoadedGames = []
        
        # open file and read the content in a list
        #with open(self.configuration.outputFile, 'r') as filehandle:
        #    for line in filehandle:
        #        # remove linebreak which is the last character of the string
        #        currentGame = line[:-1]
        
        #        # add item to the list
        #        myPreLoadedGames.append(currentGame)
        
        #for currentGameChecking in myPreLoadedGames:
        executionCommand = self.getExeCommand(game_id, self.local_game_cache)
        #print(executionCommand)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.runMySelectedGameHere,executionCommand)
        logging.info("returned")
        #print(returnedValue)
        #process = subprocess.Popen([executionCommand])
            
    
def main():
    create_and_run_plugin(GenericEmulatorPlugin, sys.argv)

# run plugin event loop
if __name__ == "__main__":
    main()