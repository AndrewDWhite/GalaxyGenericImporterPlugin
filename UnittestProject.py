'''
Created on May 9, 2020

@author: Andrew David White
'''
import unittest, logging
import asyncio
import os
from shutil import rmtree

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
        self.assertEqual(len(systems.loaded_systems_configuration),18)
    
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
        systems=setup_folders_for_testing(self)
        data = systems.list_all_recursively("test_user")
        systems.write_to_cache(data)
        self.assertTrue(systems.cache_exists())
        data_read = systems.read_from_cache()
        systems.delete_cache()
        self.assertEqual(0,len(data_read ))
        self.assertEqual(data_read, data)
            
    def test_rec(self):
        systems = ListGames()
        myresult = systems.list_all_recursively("test_user")
        #print(myresult)
        #print(len(myresult))
        #TODO implement tests
        self.assertEqual(194,len(myresult))
        
    def test_comp(self):
        systems = ListGames()
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
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),194)
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
        systems = ListGames()
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
        self.assertEqual(len(myresult["old"].keys() - myresult["new"].keys()),194)
        #None Added
        self.assertEqual(len(myresult["new"].keys() - myresult["old"].keys()),0)

        #print(myresult)
        
    def test_launch_command(self):
        systems = ListGames()
        myresult = systems.list_all_recursively("test_user")
        execution_command = get_exe_command(myresult[0]["hash_digest"], myresult)
        #print(execution_command)
        #run_my_selected_game_here(execution_command)
        #TODO implement tests
        self.assertEqual(execution_command,"\"\"%APPDATA%\\RetroArch\\retroarch.exe\" -f -L \"%APPDATA%\\RetroArch\\cores\\flycast_libretro.dll\" \"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi\"\"")
    
    def test_returned_dir_data(self):
        systems = ListGames()
        myresult = systems.list_all_recursively("test_user")[0]
        
        #print(myresult)
        expected_attributes = ["name", "execution", "path_regex", "filename_regex",
                               "game_name_regex", "game_name_regex_group",
                               "hash_digest", "filename", "filename_short",
                               "game_filename", "game_name", "path",
                               "tags"]
        self.assertEqual(len(myresult), len(expected_attributes))
        for attribute_expected in expected_attributes:
            self.assertTrue(attribute_expected in myresult)
        self.assertEqual(myresult["filename"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi")
        self.assertEqual(myresult["filename_short"],"disc.gdi")
        self.assertEqual(myresult["game_filename"],"disc")
        self.assertEqual(myresult["game_name"],"Gauntlet Legends")
        self.assertEqual(myresult["name"],"dreamcast")
        self.assertEqual(myresult["tags"],["retroarch","dreamcast"])
        self.assertEqual(myresult["path"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends")
        self.assertEqual(myresult["hash_digest"],"af6d2857d1f332323ce954ace3ec5200fe013473")
            
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

def setup_folders_for_testing (self):
    mypath = os.getcwd() + "\\TestDirectory"
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
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            updated_emulated_system["path_regex"].append(new_path)
            counter=counter+1
        updatedconfigs.append(updated_emulated_system)
    systems.loaded_systems_configuration=updatedconfigs
    return systems  

def insert_file_into_folder (self,systems,folder,file):
    for emulated_system in systems.loaded_systems_configuration:
        counter=0
        #logging.warning(emulated_system)
        for current_path in emulated_system["path_regex"]:
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
                with open(current_path+"\\"+file, 'w') as file_pointer:
                    #logging.warning("Writing")
                    #logging.warning(current_path+"\\"+file)
                    pass
                break
            counter=counter+1


class TestParameterized(unittest.TestCase):
    
    @parameterized.expand([
        ["dreamcast valid entry", "dreamcast0", "disc.gdi",1],
        ["dreamcast invalid entry", "dreamcast0", "mygame.gdi",0],
        ["dreamcast invalid path", "dreamcast1", "disc.gdi",0],
        ["gba valid entry", "gba0", "mygame.gba",1],
        ["gbc valid entry", "gbc0", "mygame.gb",1],
        ["gbc valid entry alternate extension", "gbc0", "mygame.gbc",1],
        ["gbc valid entry", "gbc1", "mygame.gb",1],
        ["gbc valid entry alternate extension", "gbc1", "mygame.gbc",1],
        ["gcn valid entry", "gcn0", "mygame.iso",1],
        ["genesis valid entry", "genesis0", "mygame.bin",1],
        ["n64 valid entry", "n640", "mygame.z64",1],
        ["nds valid entry", "nds0", "mygame.nds",1],
        ["nes valid entry", "nes0", "mygame.nes",1],
        ["ps2 valid entry", "ps20", "mygame.iso",1],
        ["ps2 valid entry", "ps20", "mygame.bin",1],
        #to do PS3 to be added ["ps3 valid entry", "ps30", "eboot.bin",1],
        ["psp valid entry", "psp0", "mygame.iso",1],
        ["ps1 valid entry", "ps10", "mygame.iso",1],
        ["ps1 valid entry", "ps10", "mygame.toc",1],
        ["snes valid entry", "snes0", "mygame.sfc",1],
        ["wii valid entry", "wii0", "mygame.iso",1],
        ["xbox valid entry", "xbox0", "default.xbe",1],
        #to do wiiu to be added ["wiiu valid entry", "wiiu0", "mygame.rpx",1],
        ["arcade valid entry", "arcade0", "mygame.zip",1],
        #to do amazon ["amazon ignored entry", "amazon0", "dxwebsetup.exe",0],
        #to do amazon ["amazon valid entry", "amazon0", "mygame.exe",1],
        #to do amazon ["amazon ignored entry", "amazon1", "dxwebsetup.exe",0],
        #to do amazon ["amazon valid entry", "amazon1", "mygame.exe",1],
    ])    
    def test_write_data_in_folders(self, name, folder, file, size):
        systems=setup_folders_for_testing(self)
        #todo insert function with parameterized files in folders
        insert_file_into_folder (self,systems,folder,file)
        data = systems.list_all_recursively("test_user")
        systems.write_to_cache(data)
        self.assertTrue(systems.cache_exists())
        data_read = systems.read_from_cache()
        systems.delete_cache()
        self.assertEqual(size,len(data_read ))
        self.assertEqual(data_read, data)

 
if __name__ == '__main__':
    unittest.main()