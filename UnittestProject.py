'''
Created on May 9, 2020

@author: Andrew David White
'''
import unittest, logging
import asyncio

#local
from configuration import DefaultConfig
from ListGames import ListGames
from generic import GenericEmulatorPlugin, get_exe_command, run_my_selected_game_here
from Backend import Backend, get_state_changes, time_delta_calc_minutes, update_local_games

from datetime import datetime

from galaxy.api.consts import LocalGameState

class UnittestProject(unittest.TestCase):
    '''
    classdocs
    '''
        
    def test_config(self):
        config = DefaultConfig()
        #TODO implement tests
        self.assertEquals(config.my_user_to_gog,"andyn")
        
    def test_emulators(self):
        systems = ListGames()
        #tests if it loaded the default number of emulators
        self.assertEqual(len(systems.loaded_systems_configuration),17)
    
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
    
    def test_write(self):
        systems = ListGames()
        systems.delete_cache()
        data = systems.list_all_recursively("test_user")
        systems.write_to_cache(data)
        self.assertTrue(systems.cache_exists())
        data_read = systems.read_from_cache()
        
        systems.delete_cache()
        self.assertEquals(184,len(data_read ))
        self.assertEquals(data_read, data)
        
    def test_rec(self):
        systems = ListGames()
        myresult = systems.list_all_recursively("test_user")
        #print(myresult)
        #print(len(myresult))
        #TODO implement tests
        self.assertEquals(184,len(myresult))
        
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
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==0)
        #All Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==184)
        #print(myresult)
    
    def test_time_delta_calc_minutes(self):
        my_delta = time_delta_calc_minutes(datetime.now())
        self.assertEquals(my_delta,0)
        
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
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==0)
        #None Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==0)

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
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==184)
        #None Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==0)

        #print(myresult)
        
    def test_launch_command(self):
        systems = ListGames()
        myresult = systems.list_all_recursively("test_user")
        execution_command = get_exe_command(myresult[0]["hash_digest"], myresult)
        #print(execution_command)
        #run_my_selected_game_here(execution_command)
        #TODO implement tests
        self.assertEquals(execution_command,"\"\"%APPDATA%\\RetroArch\\retroarch.exe\" -f -L \"%APPDATA%\\RetroArch\\cores\\flycast_libretro.dll\" \"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi\"\"")
    
    def test_returned_dir_data(self):
        systems = ListGames()
        myresult = systems.list_all_recursively("test_user")[0]
        
        #print(myresult)
        expected_attributes = ["name", "execution", "path_regex", "filename_regex",
                               "game_name_regex", "game_name_regex_group",
                               "hash_digest", "filename", "filename_short",
                               "game_filename", "game_name", "path",
                               "tags"]
        self.assertEquals(len(myresult), len(expected_attributes))
        for attribute_expected in expected_attributes:
            self.assertTrue(attribute_expected in myresult)
        self.assertEquals(myresult["filename"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi")
        self.assertEquals(myresult["filename_short"],"disc.gdi")
        self.assertEquals(myresult["game_filename"],"disc")
        self.assertEquals(myresult["game_name"],"Gauntlet Legends")
        self.assertEquals(myresult["name"],"dreamcast")
        self.assertEquals(myresult["tags"],["retroarch","dreamcast"])
        self.assertEquals(myresult["path"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends")
        self.assertEquals(myresult["hash_digest"],"af6d2857d1f332323ce954ace3ec5200fe013473")
            
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
       
if __name__ == '__main__':
    unittest.main()