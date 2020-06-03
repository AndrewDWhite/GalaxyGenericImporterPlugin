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
import pickle

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
        self.cache_filepath = os.path.abspath(os.path.join(os.path.abspath(__file__),'..','game_cache'))
        with open(emulator_config_path, 'r') as config:
            parsed_json = json.load(config)
        config.close()
        self.loaded_systems_configuration=parsed_json["systems"]
        logging.info("loading emulators configuration completed")
        logging.info(len(self.loaded_systems_configuration))
    
    def write_to_cache(self, data):
        self.write_to_cache_file(data, self.cache_filepath)
        
    def write_to_cache_file(self, data, cache_filepath):
        logging.info(cache_filepath)
        with open(cache_filepath, 'wb') as my_file:
            pickle.dump(data, my_file)
        my_file.close()
        
    def cache_exists(self):
        return self.cache_exists_file(self.cache_filepath)
    
    def cache_exists_file(self, cache_filepath):
        return os.path.exists(cache_filepath)
        
    def read_from_cache(self):
        return self.read_from_cache_filename(self.cache_filepath)
    
    def read_from_cache_filename(self, cache_filepath):
        if self.cache_exists():
            with open(cache_filepath, 'rb') as my_file:
                return pickle.load(my_file)
        else:
            return []
    
    def delete_cache(self):
        self.delete_cache_file(self.cache_filepath)
        
    def delete_cache_file(self, cache_filepath):
        if self.cache_exists():
            os.remove(cache_filepath)
    
    def hash_data(self, my_game, salt):
        myhasher = hashlib.sha1()
        myhasher.update((my_game+salt).encode('utf-8'))
        return myhasher.hexdigest()
    
    def setup_tags(self, emulated_system):
        tags = []
        if "tags" in emulated_system:
            tags = emulated_system["tags"]
        tags.append(emulated_system["name"])
        return tags
    
    def setup_entry(self, emulated_system, my_game, salt, matcher, tags):
        new_entry = emulated_system.copy()
        new_entry["hash_digest"]=self.hash_data(my_game,salt)
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
            logging.info("Could not match")
            new_entry["game_name"] = my_game
            logging.info(my_game)
            raise UserWarning("Could not match")
        new_entry["path"]=os.path.split(my_game)[0]
        new_entry["tags"] = tags
        return new_entry
    
    def list_all_recursively(self, salt):
        logging.info("listing")
        self.mylist=[]
        for emulated_system in self.loaded_systems_configuration:
            tags = self.setup_tags(emulated_system)
            matcher = re.compile(emulated_system["game_name_regex"], re.IGNORECASE)
            
            for extension in emulated_system["filename_regex"]:
                for current_path in emulated_system["path_regex"]:
                    found_games=glob.glob(os.path.join((current_path), '**',extension),recursive=True)
                    
                    for my_game in found_games:
                        try:
                            new_entry = self.setup_entry(emulated_system, my_game, salt, matcher, tags)                        
                            self.mylist.append(new_entry)
                        except  UserWarning as my_user_warning:
                            logging.info("skipping / dropping")
                            logging.info(my_user_warning)
        return self.mylist      
