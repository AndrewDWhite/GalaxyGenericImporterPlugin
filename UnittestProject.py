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

#local
from configuration import DefaultConfig
from ListGames import ListGames
from generic import GenericEmulatorPlugin, get_exe_command, run_my_selected_game_here
from Backend import Backend, get_state_changes, time_delta_calc_minutes, update_local_games,\
    create_game

from datetime import datetime

from galaxy.api.consts import LocalGameState, LicenseType

from parameterized import parameterized
from galaxy.api.types import LicenseInfo

class UnittestProject(unittest.TestCase):
    '''
    classdocs
    '''
        
    def test_config(self):
        config = DefaultConfig()
        #TODO implement tests
        self.assertEqual(config.my_user_to_gog,"username1")
        
    def test_emulators(self):
        systems = ListGames()
        #tests if it loaded the default number of emulators
        self.assertEqual(len(systems.loaded_systems_configuration),19)
    
    def test_speed(self):
        systems = ListGames()
        my_initial_time = datetime.now()
        #print (my_initial_time)
        systems.list_all_recursively("test_user")
        #my_delta = GenericEmulatorPlugin.time_delta_calc_minutes(my_initial_time)
        #print (datetime.now())
        #TODO add some test here
    
    def test_load_empty(self):
        systems = ListGames()
        systems.delete_cache()
        self.assertEqual([], systems.read_from_cache())
    
    def test_write_no_data_in_folders(self):
        systems=setup_folders_for_testing(self, "TestDirectory7")
        data = systems.list_all_recursively("test_user")
        systems.write_to_cache(data)
        self.assertTrue(systems.cache_exists())
        data_read = systems.read_from_cache()
        systems.delete_cache()
        self.assertEqual(0,len(data_read ))
        self.assertEqual(data_read, data)
            
    def test_rec(self):
        systems=setup_folders_for_testing(self, "TestDirectory5")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","")

        myresult = systems.list_all_recursively("test_user")
        #print(myresult)
        #print(len(myresult))
        #TODO implement tests
        self.assertEqual(3,len(myresult))
        
    def test_comp(self):
        systems=setup_folders_for_testing(self, "TestDirectory3")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")
        
        new_local = systems.list_all_recursively("test_user")
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = get_state_changes([],new_local)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEqual(len(myresult["old"].keys() - myresult["new"].keys()),0)
        #All Added
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),3)
        #print(myresult)
    
    def test_time_delta_calc_minutes(self):
        my_delta = time_delta_calc_minutes(datetime.now())
        self.assertEqual(my_delta,0)
        
    def test_compSame(self):
        systems = ListGames()
        new_local = systems.list_all_recursively("test_user")
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = get_state_changes(new_local,new_local)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEqual(len(myresult["old"].keys() - myresult["new"].keys()),0)
        #None Added
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),0)

        #print(myresult)
        
    def test_compRemoved(self):
        systems=setup_folders_for_testing(self, "TestDirectory8")
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        insert_file_into_folder (self, systems, "gbc0", "game.gb","")
        insert_file_into_folder (self, systems, "dos0", "game.exe","mygame")

        new_local = systems.list_all_recursively("test_user")
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = get_state_changes(new_local,[])
        #All Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEqual(len(myresult["old"].keys() - myresult["new"].keys()),3)
        #None Added
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),0)

        #print(myresult)
        
    def test_launch_command(self):
        #systems = ListGames()
        systems=setup_folders_for_testing(self, "TestDirectory4")
        insert_file_into_folder (self, systems, "dreamcast0", "disc.gdi","mygame")

        myresult = systems.list_all_recursively("test_user")
        self.assertEqual(True, len(myresult) >0 )
        execution_command = get_exe_command(myresult[0]["hash_digest"], myresult)
        #print(execution_command)
        #run_my_selected_game_here(execution_command)
        #TODO implement tests
        self.assertEqual(execution_command,"\"\"%APPDATA%\\RetroArch\\retroarch.exe\" -f -L \"%APPDATA%\\RetroArch\\cores\\flycast_libretro.dll\" \"" + os.path.abspath(os.path.join(os.path.abspath(__file__),'..',"TestDirectory4\\dreamcast0\\mygame\\disc.gdi")) + "\"\"")
    
    def test_setup_and_shutdown_folder_listeners(self):
        systems=setup_folders_for_testing(self, "TestDirectory9")
        systems.setup_folder_listeners()
        insert_file_into_folder (self, systems, "gbc0", "mygame.gb","")
        self.assertEqual(41, len(systems.my_folder_monitor_threads) )
        systems.shutdown_folder_listeners()
        self.assertEqual(True, systems.update_list_pending)
        
    
    def test_returned_dir_data(self):
        systems=setup_folders_for_testing(self, "TestDirectory6")
        insert_file_into_folder (self, systems, "dreamcast0", "disc.gdi","mygame")
        
        myresults = systems.list_all_recursively("test_user")
        self.assertEqual(True, len(myresults) >0 )
        myresult = myresults[0]
        
        #print(myresult)
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
    
    
    def test_launch_thread(self):
        self.my_game_lister = ListGames()
        self.local_game_cache = self.my_game_lister.list_all_recursively("test_user")
        self.my_authenticated = "test_user"
        self.configuration = DefaultConfig()                
        self.backend = Backend(self.configuration)        
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
    
    def test_create_game(self):
        game_dictionary = {}
        game_dictionary["hash_digest"]="hash_digest"
        game_dictionary["game_name"]="Game_Name"
        game_result = create_game(game_dictionary)
        self.assertEqual(game_result.game_id,"hash_digest")
        self.assertEqual(game_result.game_title,"Game_Name")
        self.assertEqual(game_result.dlcs,None)
        self.assertEqual(game_result.license_info,LicenseInfo(LicenseType.SinglePurchase))
        
    def test_insert_file_into_folder_watch(self): 
        my_dir = "TestDirectory2"
        systems=setup_folders_for_testing(self, my_dir)
        
        my_dir_path = os.getcwd() + "\\"+ my_dir
        
        path = "thread"
        my_full_path = my_dir_path +"\\"+path
        file = "disc.gdi"
        if os.path.exists(my_full_path):
            rmtree(my_full_path)
        os.mkdir(my_full_path)
        
        my_thread = threading.Thread(target=systems.watcher_update, args=( my_full_path, ))
        my_thread.start()
        time.sleep(2)
        #new file
        with open(my_full_path+"\\"+file, 'w') as file_pointer:
                    #logging.warning("Writing")
                    #logging.warning(current_path+"\\"+file)
                    pass
        time.sleep(1)
        #no change
        with open(my_full_path+"\\"+file, 'w') as file_pointer:
                    #logging.warning("Writing")
                    #logging.warning(current_path+"\\"+file)
                    pass
        time.sleep(1)
        #second new file
        with open(my_full_path+"\\"+file+"2", 'w') as file_pointer:
                    #logging.warning("Writing")
                    #logging.warning(current_path+"\\"+file)
                    pass
        time.sleep(4)
        
        systems.disable_monitoring()
        #new file after monitoring stopped
        #time.sleep(1)
        #with open(my_full_path+"\\"+file+"3", 'w') as file_pointer:
                    #logging.warning("Writing")
                    #logging.warning(current_path+"\\"+file)
        #            pass
        time.sleep(1)
        my_thread.join()
        #todo add testing
        self.assertEqual(True, systems.update_list_pending)

def setup_folders_for_testing (self, my_test_dir):
    mypath = os.getcwd() + "\\" + my_test_dir
    logging.debug(mypath)
    if os.path.exists(mypath):
        rmtree(mypath)
    os.mkdir(mypath)
    systems = ListGames()
    #self.cache_filepath = os.path.abspath(mypath,'..','game_cache')
    systems.delete_cache()
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
        #logging.warning(emulated_system)
        for current_path_entry in emulated_system["path_regex"]:
            current_path = current_path_entry
            #logging.warning("Path")
            #logging.warning(current_path)
            #logging.warning("Name")
            #logging.warning(emulated_system["name"])
            #logging.warning("Counter")
            #logging.warning(counter)
            #logging.warning("Folder")
            #logging.warning(folder)
            #logging.warning("Evaluating")
            #logging.warning(emulated_system["name"]+str(counter))
            if (emulated_system["name"]+str(counter)) == folder:
                #logging.warning("true")
                #logging.error(subfolder)
                if len(subfolder)>0:
                    current_path=current_path+"\\"+subfolder
                    if not os.path.exists(current_path):
                        os.mkdir(current_path)
                else:
                    logging.debug(current_path)
                #logging.error(current_path)
                with open(current_path+"\\"+file, 'w') as file_pointer:
                    #logging.warning("Writing")
                    #logging.warning(current_path+"\\"+file)
                    pass
                break
            counter=counter+1
    

class TestParameterized(unittest.TestCase):
    
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
        
    def test_write_data_in_folders(self, name, folder, file, subfolder, size):
        logging.debug(name)
        logging.debug(folder)
        logging.debug(file)
        logging.debug(size)
        
        systems=setup_folders_for_testing(self, "TestDirectory")
        #todo insert function with parameterized files in folders
        insert_file_into_folder (self, systems, folder, file, subfolder)
        data = systems.list_all_recursively("test_user")
        systems.write_to_cache(data)
        self.assertTrue(systems.cache_exists())
        data_read = systems.read_from_cache()
        systems.delete_cache()
        self.assertEqual(size, len(data_read ))
        self.assertEqual(data_read, data)

 
if __name__ == '__main__':
    unittest.main()