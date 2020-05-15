'''
Created on May 9, 2020

@author: Andrew David White
'''
import unittest, logging

#local
from configuration import DefaultConfig
from ListGames import ListGames
from generic import GenericEmulatorPlugin

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
        
    def test_rec(self):
        systems = ListGames()
        myresult = systems.list_all_recursively()
        print(len(myresult))
        #TODO implement tests
        self.assertEquals(184,len(myresult))
        
    def test_comp(self):
        systems = ListGames()
        new_local = systems.list_all_recursively()
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,[],new_local)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==0)
        #All Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==184)

        #print(myresult)
        
    def test_compSame(self):
        systems = ListGames()
        new_local = systems.list_all_recursively()
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,new_local,new_local)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==0)
        #None Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==0)

        #print(myresult)
        
    def test_compRemoved(self):
        systems = ListGames()
        new_local = systems.list_all_recursively()
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,new_local,[])
        #All Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==184)
        #None Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==0)

        #print(myresult)
        
    def test_launch_command(self):
        systems = ListGames()
        myresult = systems.list_all_recursively()
        execution_command = GenericEmulatorPlugin.getExeCommand(self,myresult[0]["hash_digest"], myresult)
        #print(execution_command)
        #GenericEmulatorPlugin.runMySelectedGameHere(self, execution_command)
        #TODO implement tests
        self.assertEquals(execution_command,"\"\"%USERPROFILE%\\AppData\\Roaming\\RetroArch\\retroarch.exe\" -f -L \"%USERPROFILE%\\AppData\\Roaming\\RetroArch\\cores\\flycast_libretro.dll\" \"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi\"\"")
    
    def test_returned_dir_data(self):
        systems = ListGames()
        myresult = systems.list_all_recursively()[0]
        
        #print(myresult)
        self.assertEquals(len(myresult), 9)
        self.assertEquals(myresult["filename"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi")
        self.assertEquals(myresult["filename_short"],"disc.gdi")
        self.assertEquals(myresult["gamename"],"disc")
        self.assertEquals(myresult["name"],"dreamcast")
        self.assertEquals(myresult["path"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends")
        self.assertEquals(myresult["hash_digest"],"50b3bc6339b0965795a61c33bbb0681966fd1752")
            
    def test_launch(self):
        systems = ListGames()
        myresult = systems.list_all_recursively()
        execution_command = GenericEmulatorPlugin.getExeCommand(self,"b96bc8c22d1ad87eb934fedf1a075ab4bf70728c", myresult)
        GenericEmulatorPlugin.runMySelectedGameHere(self, execution_command)
        #TODO implement tests
        self.assertTrue(True)
        
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s')
    unittest.main()