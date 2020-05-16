'''
Created on May 9, 2020

@author: Andrew David White
'''
import glob
import os
import json
import logging

import hashlib

class ListGames():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''        
        logging.info("loading emulators configuration")
        emulator_config_path = os.path.abspath(os.path.join(os.path.abspath(__file__),'..','emulators.json'))
        with open(emulator_config_path, 'r') as config:
            parsed_json = json.load(config)
        self.loaded_systems_configuration=parsed_json["systems"]
        logging.info("loading emulators configuration completed")
        logging.info(len(self.loaded_systems_configuration))
        
    def list_all_recursively(self):
        logging.info("listing")
        self.mylist=[]
        for emulated_system in self.loaded_systems_configuration:
            tags = []
            if "tags" in emulated_system:
                tags = emulated_system["tags"]
            tags.append(emulated_system["name"])
            
            for extension in emulated_system["filename_regex"]:
                found_games=glob.glob(os.path.join((emulated_system["path_regex"]), '**',extension),recursive=True)
                
                for my_game in found_games:
                    #with open(my_game, 'rb') as data:
                        myhasher = hashlib.sha1()
                        #logging.info(my_game)
                        new_entry = emulated_system.copy()
                        #TODO to re-enable hashing
                        #for chunk in iter(lambda: data.read(4096), ""):
                        #    myhasher.update(chunk)
                        myhasher.update(my_game.encode('utf-8'))
                        new_entry["hash_digest"]=myhasher.hexdigest()
                        #print(new_entry["hash_digest"])
                        new_entry["filename"]=my_game
                        new_entry["filename_short"]=os.path.basename(my_game)
                        new_entry["gamename"]=os.path.splitext(new_entry["filename_short"])[0]
                        new_entry["path"]=os.path.split(my_game)[0]
                        new_entry["tags"] = tags                        
                        self.mylist.append(new_entry)
        return self.mylist        