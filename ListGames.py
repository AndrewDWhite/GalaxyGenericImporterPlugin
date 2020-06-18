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
import threading
import sys

from enum import EnumMeta

class System(EnumMeta):
    WINDOWS = 1

if sys.platform == 'win32':
    SYSTEM = System.WINDOWS

if SYSTEM == System.WINDOWS:
        win32_lib_path = os.path.abspath(os.path.join(os.path.abspath(__file__),'..'))
        os.environ['PATH'] = win32_lib_path + os.pathsep + os.environ['PATH']
        import imp
        win32file = imp.load_dynamic('win32file', win32_lib_path+'\\win32\\win32file.pyd')
        win32event = imp.load_dynamic('win32event', win32_lib_path+'\\win32\\win32event.pyd')
        my_module, my_module_filename, my_module_description = imp.find_module('win32con', [win32_lib_path+'\\win32\\lib'])#\\win32con.py
        win32con = imp.load_module('win32con', my_module, my_module_filename, my_module_description)

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
        self.continue_monitoring = True
        self.my_folder_monitor_threads = []
        self.update_list_pending = False
    
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
                    logging.info(current_path)
                    found_games=glob.glob(os.path.join(os.path.expandvars(current_path), '**',extension),recursive=True)
                    
                    for my_game in found_games:
                        try:
                            new_entry = self.setup_entry(emulated_system, my_game, salt, matcher, tags)                        
                            self.mylist.append(new_entry)
                        except  UserWarning as my_user_warning:
                            logging.info("skipping / dropping")
                            logging.info(my_user_warning)
        return self.mylist      
    
    def disable_monitoring(self):
        logging.warning("disabling monitoring")
        self.continue_monitoring = False
        
    def enable_monitoring(self):
        self.continue_monitoring = True
    
    def watcher_update(self, path_to_watch):
        logging.error("Here")
        
        change_handle = win32file.FindFirstChangeNotification (
          path_to_watch,
          0,
          win32con.FILE_NOTIFY_CHANGE_FILE_NAME
        )
        
        logging.error("starting to monitor")
        try:
            while self.continue_monitoring:
            
                result = win32event.WaitForSingleObject (change_handle, 500)
        
                if result == win32con.WAIT_OBJECT_0:
                    #something was updated
                    logging.warning("Update in folder")
                    self.update_list_pending = True
                    win32file.FindNextChangeNotification (change_handle)

        finally:
            win32file.FindCloseChangeNotification (change_handle)
            
        logging.error("done this")

    def shutdown_folder_listeners(self):
        logging.warning("shutdown folder listeners")
        self.disable_monitoring()
        for my_thread in self.my_folder_monitor_threads:
            my_thread.join()
    
    def setup_folder_listeners(self):
        logging.warning("startup folder listeners")
        for emulated_system in self.loaded_systems_configuration:
            for current_path in emulated_system["path_regex"]:
                my_thread = threading.Thread(target=self.watcher_update, args=( os.path.expandvars(current_path), ))
                self.my_folder_monitor_threads.append(my_thread)
                my_thread.start()
                