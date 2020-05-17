'''
Created on May 9, 2020

@author: Andrew David White
'''
import glob
import os
import json
import logging
import re

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
        
    def list_all_recursively(self, salt):
        logging.info("listing")
        self.mylist=[]
        for emulated_system in self.loaded_systems_configuration:
            tags = []
            if "tags" in emulated_system:
                tags = emulated_system["tags"]
            tags.append(emulated_system["name"])
            matcher = re.compile(emulated_system["game_name_regex"], re.IGNORECASE)
            
            for extension in emulated_system["filename_regex"]:
                for current_path in emulated_system["path_regex"]:
                    found_games=glob.glob(os.path.join((current_path), '**',extension),recursive=True)
                    
                    for my_game in found_games:
                        myhasher = hashlib.sha1()
                        new_entry = emulated_system.copy()
                        myhasher.update((my_game+salt).encode('utf-8'))
                        new_entry["hash_digest"]=myhasher.hexdigest()
                        logging.info(new_entry["hash_digest"])
                        new_entry["filename"]=my_game
                        new_entry["filename_short"]=os.path.basename(my_game)
                        new_entry["game_filename"]=os.path.splitext(new_entry["filename_short"])[0]
                        regex_result = matcher.search(my_game)
                        logging.info(regex_result)
                        if None is not regex_result:
                            new_entry["game_name"] = regex_result.group(emulated_system["game_name_regex_group"])
                            logging.info(new_entry["game_name"])
                        else:
                            logging.warn("Could not match so just using it")
                            new_entry["game_name"] = my_game
                        new_entry["path"]=os.path.split(my_game)[0]
                        new_entry["tags"] = tags                        
                        self.mylist.append(new_entry)
        return self.mylist        