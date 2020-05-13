'''
Created on May 9, 2020

@author: Andrew David White
'''
import glob
import os
import json
import logging

import hashlib

class List_Games():
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
        
    def listAllRecursively(self):
        logging.info("listing")
        self.mylist=[]
        #how to access
        for emulated_system in self.loaded_systems_configuration:
            #logging.info(emulated_system["name"])
            #logging.info(emulated_system["execution"])
            #logging.info(emulated_system["path_regex"])
            #logging.info(emulated_system["filename_regex"])
            #logging.info("found:")
            #logging.info(glob.glob(emulated_system["path_regex"],recursive=True))
            #logging.info(glob.glob((emulated_system["path_regex"]+'./**/'+emulated_system["filename_regex"]),recursive=True))
            for extension in emulated_system["filename_regex"]:
                #logging.info (extension)
                found_games=glob.glob(os.path.join((emulated_system["path_regex"]), '**',extension),recursive=True)
                #logging.info(len(found_games))
                
                for myGame in found_games:
                    with open(myGame, 'rb') as data:
                        myhasher = hashlib.sha1()
                        #logging.info(myGame)
                        new_entry = emulated_system.copy()
                        #TODO to re-enable hashing
                        #for chunk in iter(lambda: data.read(4096), ""):
                        #    myhasher.update(chunk)
                        myhasher.update(myGame.encode('utf-8'))
                        new_entry["hash_digest"]=myhasher.hexdigest()
                        #print(new_entry["hash_digest"])
                        new_entry["filename"]=myGame
                        new_entry["filename_short"]=os.path.basename(myGame)
                        new_entry["gamename"]=os.path.splitext(new_entry["filename_short"])[0]
                        new_entry["path"]=os.path.split(myGame)[0]
                        #logging.info(new_entry)
                        self.mylist.append(new_entry)
        return self.mylist        