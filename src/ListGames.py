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
import asyncio
from datetime import datetime

from enum import EnumMeta

class System(EnumMeta):
    WINDOWS = 1

if sys.platform == 'win32':
    SYSTEM = System.WINDOWS

if SYSTEM == System.WINDOWS:
        def fast_scandir(dirname):
            subfolders= [f.path for f in os.scandir(dirname) if (f.is_dir() and str(f).find('TestDirectory')==-1  )]
            #for dirname in list(subfolders):
            #    subfolders.extend(fast_scandir(dirname))
            return subfolders
        
        my_program_dir = os.path.abspath(os.path.join(os.path.abspath(__file__),'..'))
        my_folders = fast_scandir(my_program_dir)
        for folder in my_folders:
            os.environ['PATH'] = folder + os.pathsep + os.environ['PATH']
        
        os.environ['PATH'] = my_program_dir + os.pathsep + os.environ['PATH']
        
        win32_lib_path = os.path.abspath(os.path.join(my_program_dir,"win32"))
        
        import imp
        win32file = imp.load_dynamic('win32file', win32_lib_path+'\\win32file.pyd')
        win32event = imp.load_dynamic('win32event', win32_lib_path+'\\win32event.pyd')
        my_module, my_module_filename, my_module_description = imp.find_module('win32con', [win32_lib_path+'\\lib'])#\\win32con.py
        win32con = imp.load_module('win32con', my_module, my_module_filename, my_module_description)

class ListGames():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''        
        logging.debug("loading emulators configuration")
        emulator_config_path = os.path.abspath(os.path.join(os.path.abspath(__file__),'..','systems.json'))
        self.cache_filepath = os.path.abspath(os.path.join(os.path.abspath(__file__),'..','game_cache'))
        with open(emulator_config_path, 'r') as config:
            parsed_json = json.load(config)
        config.close()
        self.loaded_systems_configuration=parsed_json["systems"]
        logging.debug("loading emulators configuration completed")
        logging.debug(len(self.loaded_systems_configuration))
        self.continue_monitoring = True
        self.my_folder_monitor_threads = []
    
    def write_to_cache(self, data):
        self.write_to_cache_file(data, self.cache_filepath)
        
    def write_to_cache_file(self, data, cache_filepath):
        logging.debug(cache_filepath)
        with open(cache_filepath, 'wb') as my_file:
            pickle.dump(data, my_file)
        my_file.close()
        
    async def cache_exists(self):
        my_cache_exists = await self.cache_exists_file(self.cache_filepath)
        return my_cache_exists
    
    async def cache_exists_file(self, cache_filepath):
        my_path_exists = os.path.exists(cache_filepath)
        return my_path_exists
        
    async def read_from_cache(self):
        my_cache = await self.read_from_cache_filename(self.cache_filepath)
        return my_cache
    
    async def read_from_cache_filename(self, cache_filepath):
        my_cache_exists = await self.cache_exists()
        if my_cache_exists:
            with open(cache_filepath, 'rb') as my_file:
                my_cache_data = pickle.load(my_file)
                return my_cache_data
        else:
            return []
    
    async def delete_cache(self):
        await self.delete_cache_file(self.cache_filepath)
        
    async def delete_cache_file(self, cache_filepath):
        my_cache_exists = await self.cache_exists()
        if my_cache_exists:
            os.remove(cache_filepath)
    
    async def hash_data(self, my_game, salt, hashContent):       
        def hashName(self, my_game, salt):
            myhasher = hashlib.sha1()
            myhasher.update((my_game+salt).encode('utf-8'))
            my_hashed_data = myhasher.hexdigest()
            return my_hashed_data
    
        def get_hash(self, file):
            logging.debug("hashing")
            with open(file, 'rb') as data:
                myhasher = hashlib.sha1()
                read_data = data.read()
                myhasher.update(read_data)
                return myhasher.hexdigest()
                #TODO to re-enable hashing
                #for chunk in iter(lambda: data.read(4096), ""):
                #    myhasher.update(chunk)
                
        if (hashContent):
            return get_hash(self, my_game)
        else:
            return hashName(self, my_game, salt)
                            
    
    async def setup_tags(self, emulated_system):
        tags = []
        if "tags" in emulated_system:
            tags = emulated_system["tags"]
        tags.append(emulated_system["name"])
        return tags
    
    async def setup_entry(self, emulated_system, my_game, salt, matcher, tags, gameShouldBeInstalled, hashContent):
        new_entry = emulated_system.copy()
        new_entry["hash_digest"]=await self.hash_data(my_game,salt,hashContent)
        logging.debug(new_entry["hash_digest"])
        new_entry["filename"]=my_game
        new_entry["filename_short"] = os.path.basename(my_game)
        new_entry["gameShouldBeInstalled"] = gameShouldBeInstalled
        #raw_entry = os.path.splitext(new_entry["filename_short"])
        #new_entry["game_filename"] = raw_entry[0]
        regex_result = matcher.search(my_game)
        logging.debug(regex_result)
        if None is not regex_result:
            new_entry["game_name"] = regex_result.group(emulated_system["game_name_regex_group"])
            new_entry["game_filename"] = regex_result.group(emulated_system["system_rom_name_regex_group"])
            logging.debug(new_entry["game_name"])
        else:
            logging.info("Could not match")
            new_entry["game_name"] = my_game
            logging.info(my_game)
            raise UserWarning("Could not match")
        raw_path = os.path.split(my_game)
        new_entry["path"] = raw_path[0]
        new_entry["tags"] = tags
        return new_entry
    
    async def list_all_recursively (self, salt):
        myList = []
        myIterator = self.list_iterative_recursively(salt)
        while (True):
            try:
            
                myEntry = await myIterator.__anext__()
                myList.append(myEntry)
            except StopAsyncIteration:
                break
        
        return myList
    
    async def list_iterative_recursively(self, salt):
        logging.debug("listing")
        #Iterate through each system's configuration for where we should look for programs and add the metadata to results
        for emulated_system in self.loaded_systems_configuration:
            gameShouldBeInstalled = emulated_system["gameShouldBeInstalled"]
            hashContent = emulated_system["hashContent"]
            tags = await self.setup_tags(emulated_system)
            matcher = re.compile(emulated_system["game_name_regex"], re.IGNORECASE)
            
            #Below this point the data is unique for each extension and path
            for extension in emulated_system["filename_regex"]:

                for current_path in emulated_system["path_regex"]:
                    logging.debug(current_path)
                    my_path_expanded = os.path.expandvars(current_path)
                    my_path_joined = os.path.join(my_path_expanded, '**', extension)
                    logging.debug(my_path_joined)
                    begin_time = datetime.now()
                    
                    found_games = glob.iglob(my_path_joined, recursive=True)
                    
                    current_time = datetime.now()
                    time_delta = (current_time - begin_time)
                    time_delta_seconds = time_delta.total_seconds()
                    logging.debug(time_delta_seconds)
                    
                    #Below here unique for each game
                    for my_game in found_games:
                        logging.debug(my_game)
                        try:
                            new_entry = await self.setup_entry(emulated_system, my_game, salt, matcher, tags, gameShouldBeInstalled, hashContent)                        
                            yield new_entry
                        except  UserWarning as my_user_warning:
                            logging.debug("skipping / dropping")
                            logging.debug(my_user_warning)
    
    def disable_monitoring(self):
        logging.debug("disabling monitoring")
        self.continue_monitoring = False
    
    def watcher_update(self, path_to_watch, my_queue_folder_awaiting_scan):
        logging.debug("watcher update")
        
        #Monitor the directories if they exist TODO determine if we also want to monitor them if they don't
        if (os.path.exists(path_to_watch)) :
            logging.debug ("EXISTS")
            change_handle = win32file.FindFirstChangeNotification (
              path_to_watch,
              True, #watch tree
              win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | win32con.FILE_NOTIFY_CHANGE_DIR_NAME | win32con.FILE_NOTIFY_CHANGE_SIZE | win32con.FILE_NOTIFY_CHANGE_SECURITY 
            )
            
            logging.debug("starting to monitor")
            logging.debug(path_to_watch)
            try:
                while self.continue_monitoring:
                    logging.debug("still monitoring")
                    logging.debug(path_to_watch)
                    result =  win32event.WaitForSingleObject (change_handle, 500)
            
                    if result == win32con.WAIT_OBJECT_0:
                        #something was updated
                        logging.debug("Update in folder")
                        logging.debug(path_to_watch)
                        my_queue_folder_awaiting_scan.put(path_to_watch)
                        win32file.FindNextChangeNotification (change_handle)
    
            finally:
                win32file.FindCloseChangeNotification (change_handle)
        logging.debug("done this")

    async def shutdown_folder_listeners(self):
        logging.debug("shutdown folder listeners")
        self.disable_monitoring()
        for my_thread in self.my_folder_monitor_threads:
            logging.debug("shutting down thread")
            logging.debug(my_thread)
            while (my_thread.is_alive()):
                await asyncio.sleep(1)
            #TODO cleanup nicer
            #my_thread.join()
    
    async def setup_folder_listeners(self, my_queue_folder_awaiting_scan):
        logging.debug("startup folder listeners")
        for emulated_system in self.loaded_systems_configuration:
            for current_path in emulated_system["path_regex"]:
                logging.debug("listening to")
                logging.debug(current_path)
                my_thread = threading.Thread(target=self.watcher_update, args=( os.path.expandvars(current_path), my_queue_folder_awaiting_scan, ))
                self.my_folder_monitor_threads.append(my_thread)
                my_thread.daemon = True
                my_thread.start()
                

