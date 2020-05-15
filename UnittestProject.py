'''
Created on May 9, 2020

@author: Andrew David White
'''
import unittest

#local
from configuration import Default_Config
from ListGames import ListGames
from generic import GenericEmulatorPlugin

from galaxy.api.consts import LocalGameState
from galaxy.api.consts import Platform

class UnittestProject(unittest.TestCase):
    '''
    classdocs
    '''
        
    def test_config(self):
        Default_Config()
        #TODO implement tests
        self.assertTrue(True)
        
    def test_emulators(self):
        systems = ListGames()
        #tests if it loaded the default number of emulators
        self.assertEqual(len(systems.loaded_systems_configuration),17)
        
    def test_rec(self):
        systems = ListGames()
        myresult = systems.list_all_recursively(Platform.Test)
        print(len(myresult))
        #TODO implement tests
        self.assertNotEquals(184,len(myresult))
        self.assertEquals(112,len(myresult))
        
    def test_comp(self):
        systems = ListGames()
        new_local = systems.list_all_recursively(Platform.Test)
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,[],new_local)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEquals(len(myresult["old"].keys() - myresult["new"].keys()),0)
        #All Added
        self.assertEquals(len(myresult["new"].keys() - myresult["old"].keys()),112)

        #print(myresult)
        
    def test_compSame(self):
        systems = ListGames()
        new_local = systems.list_all_recursively(Platform.Test)
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,new_local,new_local)
        #None Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEquals(len(myresult["old"].keys() - myresult["new"].keys()),0)
        #None Added
        self.assertEquals(len(myresult["new"].keys() - myresult["old"].keys()),0)

        #print(myresult)
        
    def test_compRemoved(self):
        systems = ListGames()
        new_local = systems.list_all_recursively(Platform.Test)
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,new_local,[])
        #All Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEquals(len(myresult["old"].keys() - myresult["new"].keys()),112)
        #None Added
        self.assertEquals(len(myresult["new"].keys() - myresult["old"].keys()),0)

        #print(myresult)
        
    def test_compRemovedNes(self):
        systems = ListGames()
        new_local = systems.list_all_recursively(Platform.NintendoEntertainmentSystem)
        for entry in new_local:
            #print("Check")
            if("local_game_state" not in entry):
                #print("should")
                entry["local_game_state"]=LocalGameState.Installed
        myresult = GenericEmulatorPlugin.get_state_changes(self,new_local,[])
        #All Removed
        #print (len(myresult["old"].keys() - myresult["new"].keys()))
        #print (len(myresult["new"].keys() - myresult["old"].keys()))
        self.assertEquals(len(myresult["old"].keys() - myresult["new"].keys()),12) #161
        #None Added
        self.assertEquals(len(myresult["new"].keys() - myresult["old"].keys()),0)

        #print(myresult)
        
    def test_launch_command(self):
        systems = ListGames()
        myresult = systems.list_all_recursively(Platform.Test)
        execution_command = GenericEmulatorPlugin.getExeCommand(self,myresult[0]["hash_digest"], myresult)
        #print(execution_command)
        #GenericEmulatorPlugin.runMySelectedGameHere(self, execution_command)
        #TODO implement tests
        self.assertEquals(execution_command,"\"\"%USERPROFILE%\\AppData\\Roaming\\RetroArch\\retroarch.exe\" -f -L \"%USERPROFILE%\\AppData\\Roaming\\RetroArch\\cores\\flycast_libretro.dll\" \"F:\\Software\\games\\roms\\Dreamcast\\Gauntlet Legends\\disc.gdi\"\"")
    
    def test_returned_dir_data(self):
        systems = ListGames()
        myresult = systems.list_all_recursively(Platform.Test)[0]
        
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
        myresult = systems.list_all_recursively(Platform.Test)
        execution_command = GenericEmulatorPlugin.getExeCommand(self,"b96bc8c22d1ad87eb934fedf1a075ab4bf70728c", myresult)
        GenericEmulatorPlugin.runMySelectedGameHere(self, execution_command)
        #TODO implement tests
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()