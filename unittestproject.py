'''
Created on May 9, 2020

@author: Andrew David White
'''
import unittest
import os
import asyncio

#local
from configuration import Default_Config
from list_games import List_Games
from generic import GenericEmulatorPlugin
from _operator import length_hint

from galaxy.api.consts import LocalGameState

class unittestproject(unittest.TestCase):
    '''
    classdocs
    '''
        
    def test_config(self):
        Default_Config()
        #TODO implement tests
        self.assertTrue(True)
        
    def test_emulators(self):
        systems = List_Games()
        #tests if it loaded the default number of emulators
        self.assertEqual(len(systems.loaded_systems_configuration),17)
        
    def test_rec(self):
        systems = List_Games()
        myresult = systems.listAllRecursively()
        print(len(myresult))
        #TODO implement tests
        self.assertEquals(184,len(myresult))
        
    def test_comp(self):
        systems = List_Games()
        newLocal = systems.listAllRecursively()
        for entry in newLocal:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,[],newLocal)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==0)
        #All Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==184)

        #print(myresult)
        
    def test_compSame(self):
        systems = List_Games()
        newLocal = systems.listAllRecursively()
        for entry in newLocal:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,newLocal,newLocal)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==0)
        #None Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==0)

        #print(myresult)
        
    def test_compRemoved(self):
        systems = List_Games()
        newLocal = systems.listAllRecursively()
        for entry in newLocal:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,newLocal,[])
        #All Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertTrue(len(myresult["old"].keys() - myresult["new"].keys())==184)
        #None Added
        self.assertTrue(len(myresult["new"].keys() - myresult["old"].keys())==0)

        #print(myresult)
        
    def test_launch_command(self):
        systems = List_Games()
        myresult = systems.listAllRecursively()
        executionCommand = GenericEmulatorPlugin.getExeCommand(self,myresult[0]["hash_digest"], myresult)
        #print(executionCommand)
        #GenericEmulatorPlugin.runMySelectedGameHere(self, executionCommand)
        #TODO implement tests
        self.assertEquals(executionCommand,"\"\"C:\\Users\\andyn\\AppData\\Roaming\\RetroArch\\retroarch.exe\" -f -L \"C:\\Users\\andyn\\AppData\\Roaming\\RetroArch\\cores\\flycast_libretro.dll\" \"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi\"\"")
    
    def test_returned_dir_data(self):
        systems = List_Games()
        myresult = systems.listAllRecursively()[0]
        
        #print(myresult)
        self.assertEquals(len(myresult), 9)
        self.assertEquals(myresult["filename"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi")
        self.assertEquals(myresult["filename_short"],"disc.gdi")
        self.assertEquals(myresult["gamename"],"disc")
        self.assertEquals(myresult["name"],"dreamcast")
        self.assertEquals(myresult["path"],"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends")
        self.assertEquals(myresult["hash_digest"],"50b3bc6339b0965795a61c33bbb0681966fd1752")
            
    def test_launch(self):
        systems = List_Games()
        myresult = systems.listAllRecursively()
        executionCommand = GenericEmulatorPlugin.getExeCommand(self,"b96bc8c22d1ad87eb934fedf1a075ab4bf70728c", myresult)
        GenericEmulatorPlugin.runMySelectedGameHere(self, executionCommand)
        #TODO implement tests
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()