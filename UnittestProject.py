'''
Created on May 9, 2020

@author: Andrew David White
'''
import unittest, logging
import asyncio
import os
from shutil import rmtree

import threading
import time
import hashlib
import queue
import math

#local
from configuration import DefaultConfig
from ListGames import ListGames
from generic import GenericEmulatorPlugin, get_exe_command, run_my_selected_game_here
from Backend import Backend, get_state_changes, time_delta_calc_minutes, update_local_games_thread, create_game, shutdown_library, do_auth, removed_games, added_games, state_changed, setup_queue_to_send_those_changes, send_events, created_update, time_tracking

from datetime import datetime
import aiounittest

from galaxy.api.consts import LocalGameState, LicenseType

from parameterized import parameterized
from galaxy.api.types import LicenseInfo, Authentication

from unittest.mock import Mock, MagicMock

class UnittestProject(aiounittest.AsyncTestCase):
    '''
    classdocs
    '''
        
    async def test_config(self):
        config = DefaultConfig()
        logging.debug(config)
        self.assertEqual(config.my_user_to_gog, "username1")
        self.assertEqual(config.my_platform_to_gog, "test")
        
    async def  test_emulators(self):
        systems = ListGames()
        #tests if it loaded the default number of emulators
        self.assertEqual(len(systems.loaded_systems_configuration),21)
    
    async def test_speed(self):
        systems = ListGames()
        my_initial_time = datetime.now()
        logging.debug(my_initial_time)
        await systems.list_all_recursively ("test_user")
        #my_delta = GenericEmulatorPlugin.time_delta_calc_minutes(my_initial_time)
        #logging.debug(datetime.now())
        #TODO add some test here
    
    async def test_load_empty(self):
        systems = ListGames()
        await systems.delete_cache()
        read_cache = await systems.read_from_cache()
        self.assertEqual([], read_cache)
    
    async def test_write_no_data_in_folders(self):
        systems=await setup_folders_for_testing(self, "TestDirectory7")
        data = await systems.list_all_recursively("test_user")
        systems.write_to_cache(data)
        my_cache_exists = await systems.cache_exists()
        self.assertTrue(my_cache_exists)
        data_read = await systems.read_from_cache()
        await systems.delete_cache()
        self.assertEqual(0,len(data_read ))
        self.assertEqual(data_read, data)
            
    async def test_rec(self):
        systems=await setup_folders_for_testing(self, "TestDirectory5")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","")
        myresult = await systems.list_all_recursively("test_user")
        logging.debug(myresult)
        logging.debug(len(myresult))
        #TODO implement tests
        self.assertEqual(3,len(myresult))
        
    async def test_comp(self):
        systems=await setup_folders_for_testing(self, "TestDirectory3")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")
        new_local = await systems.list_all_recursively("test_user")
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = await get_state_changes([],new_local)
        #None Removed
        logging.debug(len(myresult["old"].keys() - myresult["new"].keys()))
        logging.debug(len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEqual(len(myresult["old"].keys() - myresult["new"].keys()),0)
        #All Added
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),3)
        logging.debug(myresult)
    
    async def test_time_delta_calc_minutes(self):
        my_delta = await time_delta_calc_minutes(datetime.now())
        self.assertEqual(my_delta,0)
        
    async def test_compSame(self):
        systems = ListGames()
        new_local = await systems.list_all_recursively("test_user")
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = await get_state_changes(new_local,new_local)
        #None Removed
        logging.debug(len(myresult["old"].keys() - myresult["new"].keys()))
        logging.debug(len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEqual(len(myresult["old"].keys() - myresult["new"].keys()),0)
        #None Added
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),0)
        logging.debug(myresult)
        
    async def test_compRemoved(self):
        systems=await setup_folders_for_testing(self, "TestDirectory14")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")
        new_local = await systems.list_all_recursively("test_user")
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = await get_state_changes(new_local,[])
        #All Removed
        logging.debug(len(myresult["old"].keys() - myresult["new"].keys()))
        logging.debug(len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEqual(len(myresult["old"].keys() - myresult["new"].keys()),3)
        #None Added
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),0)
        logging.debug(myresult)
        
    async def test_launch_command(self):
        #systems = ListGames()
        systems=await setup_folders_for_testing(self, "TestDirectory4")
        insert_file_into_folder (self, systems, "dreamcast0", "disc.gdi","mygame")
        myresult = await systems.list_all_recursively("test_user")
        self.assertEqual(True, len(myresult) >0 )
        execution_command = await get_exe_command(myresult[0]["hash_digest"], myresult)
        logging.debug(execution_command)
        #run_my_selected_game_here(execution_command)
        #TODO implement tests
        self.assertEqual(execution_command,"\"\"%APPDATA%\\RetroArch\\retroarch.exe\" -f -L \"%APPDATA%\\RetroArch\\cores\\flycast_libretro.dll\" \"" + os.path.abspath(os.path.join(os.path.abspath(__file__),'..',"TestDirectory4\\dreamcast0\\mygame\\disc.gdi")) + "\"\"")
    
    async def test_setup_and_shutdown_folder_listeners(self):
        systems=await setup_folders_for_testing(self, "TestDirectory9")
        my_queue_folder_awaiting_scan = queue.Queue()
        await systems.setup_folder_listeners(my_queue_folder_awaiting_scan)
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "dos0", "mygame.exe","mygame")
        self.assertEqual(44, len(systems.my_folder_monitor_threads) )
        systems.shutdown_folder_listeners()
        self.assertEqual(False, my_queue_folder_awaiting_scan.empty())
        self.assertEqual(os.path.abspath(os.path.join(os.path.abspath(__file__),'..',"TestDirectory9\\gbc0")),my_queue_folder_awaiting_scan.get())
        self.assertEqual(os.path.abspath(os.path.join(os.path.abspath(__file__),'..',"TestDirectory9\\dos0")),my_queue_folder_awaiting_scan.get())

    #def test_returned_real_dir_data(self):        
    #    systems = ListGames()
    #    myresults = systems.list_all_recursively("test_user")
    #    for entry in myresults:
    #        #print(entry)
    #        if "xbox 360" in entry["name"]:
    #            print(entry)
    
    async def test_returned_dir_data(self):
        systems=await setup_folders_for_testing(self, "TestDirectory6")
        insert_file_into_folder (self, systems, "dreamcast0", "disc.gdi","mygame")
        myresults = await systems.list_all_recursively("test_user")
        self.assertEqual(True, len(myresults) >0 )
        myresult = myresults[0]
        logging.debug(myresult)
        expected_attributes = ["name", "execution", "path_regex", "filename_regex",
                               "game_name_regex", "game_name_regex_group",
                               "hash_digest", "filename", "filename_short",
                               "game_filename", "game_name", "path",
                               "tags"]
        self.assertEqual(len(myresult), len(expected_attributes))
        for attribute_expected in expected_attributes:
            self.assertTrue(attribute_expected in myresult)
        self.assertEqual(myresult["filename"],os.path.abspath(os.path.join(os.path.abspath(__file__),'..',"TestDirectory6\\dreamcast0\\mygame\\disc.gdi")))
        self.assertEqual(myresult["filename_short"],"disc.gdi")
        self.assertEqual(myresult["game_filename"],"disc")
        self.assertEqual(myresult["game_name"],"mygame")
        self.assertEqual(myresult["name"],"dreamcast")
        self.assertEqual(myresult["tags"],["retroarch","dreamcast"])
        self.assertEqual(myresult["path"],os.path.abspath(os.path.join(os.path.abspath(__file__),'..',"TestDirectory6\\dreamcast0\\mygame")))
        myhasher = hashlib.sha1()
        myhasher.update((myresult["filename"]+"test_user").encode('utf-8'))
        expected_hash= myhasher.hexdigest()
        self.assertEqual(myresult["hash_digest"],expected_hash)
            
    #def test_launch(self):
    #    systems = ListGames()
    #    myresult = systems.list_all_recursively("test_user")
    #    execution_command = get_exe_command("70408a8d1da48c8760c3c65f2485f3d28c23198f", myresult)
    #    task = run_my_selected_game_here(execution_command)
    #    loop = asyncio.new_event_loop()
    #    asyncio.set_event_loop(loop)
    #    loop.run_until_complete(task)
        #TODO implement tests
    #    self.assertTrue(True)
        
    #def test_launch_game(self):
    #    systems = ListGames()
    #    self.local_game_cache = systems.list_all_recursively("test_user")
                
    #    self.my_threads = []
    #    task = GenericEmulatorPlugin.launch_game(self, "70408a8d1da48c8760c3c65f2485f3d28c23198f")
    #    loop = asyncio.new_event_loop()
    #    asyncio.set_event_loop(loop)
    #    loop.run_until_complete(task)
        #TODO implement tests
    #    self.assertTrue(True)
    
    
    async def test_launch_thread(self):
        self.my_game_lister = ListGames()
        self.local_game_cache = await self.my_game_lister.list_all_recursively("test_user")
        self.my_authenticated = "test_user"
        self.configuration = DefaultConfig()                
        self.backend = Backend()
        await self.backend.setup(self.configuration)        
        self.my_threads = []
        #GenericEmulatorPlugin.get_owned_games(self)
        #GenericEmulatorPlugin.get_local_games(self)
        #update_local_games(self, "test_user", self.my_game_lister)
        #logging.getLogger('').setLevel(logging.DEBUG)
        #GenericEmulatorPlugin.tick(self)
    #    GenericEmulatorPlugin.tick(self)
        #TODO implement tests
    #    self.assertTrue(True)
    
    logging.basicConfig(level=logging.WARN, format='%(message)s')
    # define a Handler which writes messages to the sys.stderr
    console = logging.StreamHandler()
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    
    async def test_create_game(self):
        game_dictionary = {}
        game_dictionary["hash_digest"]="hash_digest"
        game_dictionary["game_name"]="Game_Name"
        game_result = await create_game(game_dictionary)
        self.assertEqual(game_result.game_id,"hash_digest")
        self.assertEqual(game_result.game_title,"Game_Name")
        self.assertEqual(game_result.dlcs,None)
        self.assertEqual(game_result.license_info,LicenseInfo(LicenseType.SinglePurchase))
        
    async def test_insert_file_into_folder_watch(self): 
        my_dir = "TestDirectory2"
        systems=await setup_folders_for_testing(self, my_dir)
        
        my_dir_path = os.getcwd() + "\\"+ my_dir
        
        path = "thread"
        my_full_path = my_dir_path +"\\"+path
        file = "disc.gdi"
        if os.path.exists(my_full_path):
            rmtree(my_full_path)
        os.mkdir(my_full_path)
        my_queue_folder_awaiting_scan = queue.Queue()
        my_thread = threading.Thread(target=systems.watcher_update, args=( my_full_path, my_queue_folder_awaiting_scan, ))
        my_thread.start()
        time.sleep(2)
        #new file
        with open(my_full_path+"\\"+file, 'w') as file_pointer:
                    logging.debug("Writing")
                    logging.debug(my_full_path+"\\"+file)
        time.sleep(1)
        #no change
        with open(my_full_path+"\\"+file, 'w') as file_pointer:
                    logging.debug("Writing")
                    logging.debug(my_full_path+"\\"+file)
        time.sleep(1)
        #second new file
        with open(my_full_path+"\\"+file+"2", 'w') as file_pointer:
                    logging.debug("Writing")
                    logging.debug(my_full_path+"\\"+file+"2")
        time.sleep(4)
        
        systems.disable_monitoring()
        #self.local_game_cache =
        #new file after monitoring stopped
        #time.sleep(1)
        #with open(my_full_path+"\\"+file+"3", 'w') as file_pointer:
                    #logging.warning("Writing")
                    #logging.warning(current_path+"\\"+file)
        #            pass
        time.sleep(1)
        my_thread.join()
        #todo add testing
        self.assertEqual(False, my_queue_folder_awaiting_scan.empty())
        
    async def test_start_and_stop_library(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        self.my_library_thread = threading.Thread(target=update_local_games_thread, args=(self, "test_user", self.backend.my_game_lister,))
        logging.debug("starting")
        self.my_library_thread.start()
        self.assertEqual(True, self.my_library_thread.is_alive())
        self.assertEqual(True, self.backend.library_run)
        shutdown_library(self)
        self.assertEqual(False, self.my_library_thread.is_alive())
        del self.backend 
        #TODO implements tests

    async def test_removed_backend(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        
        systems=await setup_folders_for_testing(self, "TestDirectory10")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")
        new_local = await systems.list_all_recursively("test_user")
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = await get_state_changes(new_local,[])

        await removed_games(self, myresult["old"],myresult["new"])
        self.assertEqual(3, self.backend.my_queue_update_local_game_status._qsize())
        game_update_from_queue = self.backend.my_queue_update_local_game_status.get()
        self.assertEqual(game_update_from_queue.local_game_state, LocalGameState.None_)
        
    async def test_added_backend(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        
        systems=await setup_folders_for_testing(self, "TestDirectory11")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")
        new_local = await systems.list_all_recursively("test_user")
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = await get_state_changes([],new_local)
        
        await added_games(self, new_local, myresult["old"],myresult["new"])
        self.assertEqual(3, self.backend.my_queue_update_local_game_status._qsize())
        game_update_from_queue = self.backend.my_queue_update_local_game_status.get()
        self.assertEqual(game_update_from_queue.local_game_state, LocalGameState.Installed)
        
        self.assertEqual(3, self.backend.my_queue_add_game._qsize())

    async def test_no_time_updates(self):
        await time_tracking(self,[])
    
    async def test_time_updates(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        if os.path.exists(self.backend.cache_times_filepath):
            os.remove(self.backend.cache_times_filepath)
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        
        my_threads = []
        my_thread = Mock()
        my_current_time = datetime.now()
        my_thread.name="{\"time\":\""+str(my_current_time)+"\", \"id\":\"12345A\"}"
        my_thread.is_alive= MagicMock(return_value=False)
        my_threads.append(my_thread)
        await time_tracking(self,my_threads)
        
        #local_time_cache = await self.my_game_lister.read_from_cache_filename(self.backend.cache_times_filepath)
        self.assertEqual(1,len(self.backend.local_time_cache))
        my_timed_entry = self.backend.local_time_cache[0]
        
        self.assertEqual(my_timed_entry["run_time_total"], 1)
        self.assertEqual(my_timed_entry["last_time_played"], math.floor(my_current_time.timestamp() ))
        self.assertEqual(my_timed_entry["hash_digest"], "12345A")
        
        if os.path.exists(self.backend.cache_times_filepath):
            os.remove(self.backend.cache_times_filepath)

    async def test_changed_backend(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        
        systems=await setup_folders_for_testing(self, "TestDirectory12")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")
        new_local = await systems.list_all_recursively("test_user")
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = await get_state_changes(new_local,new_local)
        myresult["old"][list(myresult["old"].keys())[0]] = LocalGameState.Running
        await state_changed(self, myresult["old"],myresult["new"])
                
        self.assertEqual(False, self.backend.my_queue_update_local_game_status.empty())
        self.assertEqual(1, self.backend.my_queue_update_local_game_status._qsize())

    async def test_setup_queue_to_send_those_changes_backend(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        
        systems=await setup_folders_for_testing(self, "TestDirectory13")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")
        new_local = await systems.list_all_recursively("test_user")
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = await get_state_changes(new_local,new_local)
        await setup_queue_to_send_those_changes(self, new_local, myresult["old"],myresult["new"])
        #No changes
        self.assertEqual(0, self.backend.my_queue_update_local_game_status._qsize())
        self.assertEqual(0, self.backend.my_queue_add_game._qsize())

    async def test_created_time_update(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        
        systems=await setup_folders_for_testing(self, "TestDirectory8")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        new_local = await systems.list_all_recursively("test_user")
        my_time = datetime.now()
        for entry in new_local:
            logging.debug("Check")
            if("local_game_state" not in entry):
                logging.debug("should")
                entry["local_game_state"]=LocalGameState.Installed
        updated_Time = await created_update(new_local[0],1,my_time)
        #New
        self.assertEqual(math.floor(my_time.timestamp() ), updated_Time["last_time_played"])
        self.assertEqual(1, updated_Time["run_time_total"])
        updated_Time = await created_update(updated_Time,1,my_time)
        #Updated
        self.assertEqual(math.floor(my_time.timestamp() ), updated_Time["last_time_played"])
        self.assertEqual(2, updated_Time["run_time_total"])

    
    async def test_no_updates_send(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        await send_events(self)
    
    async def test_do_auth(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration) 
        self.store_credentials = Mock(return_value=None)
        
        authenticated_user = await do_auth(self, "test_user")
        self.assertEqual(Authentication('importer_user', "test_user"), authenticated_user)
        self.assertEqual(self.backend.my_authenticated, True) 
        user_data = {}
        user_data['username'] = "test_user"
        self.store_credentials.assert_called_with(user_data)
        
async def setup_folders_for_testing (self, my_test_dir):
    mypath = os.getcwd() + "\\" + my_test_dir
    logging.debug(mypath)
    if os.path.exists(mypath):
        rmtree(mypath)
    os.mkdir(mypath)
    systems = ListGames()
    #self.cache_filepath = os.path.abspath(mypath,'..','game_cache')
    await systems.delete_cache()
    updatedconfigs=[]
    for emulated_system in systems.loaded_systems_configuration:
        updated_emulated_system=emulated_system.copy()
        updated_emulated_system["path_regex"]=[]
        counter=0
        for current_path in emulated_system["path_regex"]:
            new_path=mypath+"\\"+emulated_system["name"]+str(counter)
            logging.debug(new_path)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            updated_emulated_system["path_regex"].append(new_path)
            counter=counter+1
        updatedconfigs.append(updated_emulated_system)
    systems.loaded_systems_configuration=updatedconfigs
    return systems  

def insert_file_into_folder (self, systems, folder, file, subfolder):
    for emulated_system in systems.loaded_systems_configuration:
        counter=0
        logging.debug(emulated_system)
        for current_path_entry in emulated_system["path_regex"]:
            current_path = current_path_entry
            logging.debug("Path")
            logging.debug(current_path)
            logging.debug("Name")
            logging.debug(emulated_system["name"])
            logging.debug("Counter")
            logging.debug(counter)
            logging.debug("Folder")
            logging.debug(folder)
            logging.debug("Evaluating")
            logging.debug(emulated_system["name"]+str(counter))
            if (emulated_system["name"]+str(counter)) == folder:
                logging.debug(subfolder)
                if len(subfolder)>0:
                    current_path=current_path+"\\"+subfolder
                    if not os.path.exists(current_path):
                        os.mkdir(current_path)
                else:
                    logging.debug(current_path)
                #logging.debug(current_path)
                with open(current_path+"\\"+file, 'w') as file_pointer:
                    logging.debug("Writing")
                    logging.debug(current_path+"\\"+file)
                break
            counter=counter+1
    

class TestParameterized(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
    
    @parameterized.expand([
        ["dreamcast valid entry", "dreamcast0", "disc.gdi","mygame",1],
        ["dreamcast invalid entry", "dreamcast0", "mygame.gdi","mygame",0],
        ["dreamcast invalid path", "dreamcast2", "disc.gdi","mygame",0],
        ["gba valid entry", "gba0", "mygame.gba","",1],
        ["gbc valid entry", "gbc0", "mygame.gb","",1],
        ["gbc valid entry alternate extension", "gbc0", "mygame.gbc","",1],
        ["gbc valid entry", "gbc1", "mygame.gb","",1],
        ["gbc valid entry alternate extension", "gbc1", "mygame.gbc","",1],
        ["gcn valid entry", "gcn0", "mygame.iso","mygame",1],
        ["genesis valid entry", "genesis0", "mygame.bin","",1],
        ["n64 valid entry", "n640", "mygame.z64","",1],
        ["nds valid entry", "nds0", "mygame.nds","",1],
        ["nes valid entry", "nes0", "mygame.nes","",1],
        ["ps2 valid entry", "ps20", "mygame.iso","",1],
        ["ps2 valid entry", "ps20", "mygame.bin","",1],
        #to do PS3 to be added ["ps3 valid entry", "ps30", "eboot.bin",1],
        ["psp valid entry", "psp0", "mygame.iso","",1],
        ["ps1 valid entry", "ps10", "mygame.iso","",1],
        ["ps1 valid entry", "ps10", "mygame.toc","",1],
        ["snes valid entry", "snes0", "mygame.sfc","",1],
        ["wii valid entry", "wii0", "mygame.iso","mygame",1],
        ["xbox valid entry", "xbox0", "default.xbe","mygame",1],
        #to do wiiu to be added ["wiiu valid entry", "wiiu0", "mygame.rpx",1],
        ["arcade valid entry", "arcade0", "mygame.zip","",1],
        #to do amazon ["amazon ignored entry", "amazon0", "dxwebsetup.exe","mygame"0],
        #to do amazon ["amazon valid entry", "amazon0", "mygame.exe","mygame",1],
        #to do amazon ["amazon ignored entry", "amazon1", "dxwebsetup.exe","mygame",0],
        #to do amazon ["amazon valid entry", "amazon1", "mygame.exe","mygame",1],
    ])
    
    def test_write_data_in_folders_sync(self, name, folder, file, subfolder, size):

        async def test_write_data_in_folders(self, name, folder, file, subfolder, size):
            logging.debug(name)
            logging.debug(folder)
            logging.debug(file)
            logging.debug(size)
            
            systems=await setup_folders_for_testing(self, "TestDirectory")
            #todo insert function with parameterized files in folders
            insert_file_into_folder (self, systems, folder, file, subfolder)
            data = await systems.list_all_recursively("test_user")
            systems.write_to_cache(data)
    
            loop_result = await systems.cache_exists()
            self.assertTrue(loop_result)
            data_read = await systems.read_from_cache()
            await systems.delete_cache()
            self.assertEqual(size, len(data_read ))
            self.assertEqual(data_read, data)

        try:
            self.loop.run_until_complete(test_write_data_in_folders(self, name, folder, file, subfolder, size))
        finally:
            self.loop.close()
        
if __name__ == '__main__':
    unittest.main()