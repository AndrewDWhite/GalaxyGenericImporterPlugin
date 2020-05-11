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
        #tests if it loaded the default 16 emulators
        print(len(systems.loaded_systems_configuration))
        self.assertEqual(len(systems.loaded_systems_configuration),16)
        #TODO implement more tests
        
    def test_rec(self):
        systems = List_Games()
        myresult = systems.listAllRecursively()
        print(myresult)
        #TODO implement tests
        self.assertTrue(True)
        
    #def test_comp(self):
    #    systems = List_Games()
    #    newLocal = systems.listAllRecursively()
    #    for entry in newLocal:
    #        #print("Check")
    #        if("local_game_state" not in entry):
    #            #print("should")
    #            entry["local_game_state"]=LocalGameState.Installed
    #    myresult = GenericEmulatorPlugin.get_state_changes(self,[],newLocal)
    #    print(myresult)
    #    #TODO implement tests
    #    self.assertTrue(True)
        
    def test_launch(self):
        systems = List_Games()
        myresult = systems.listAllRecursively()
        self.local_game_cache=myresult
        print(myresult[0])
        functionLauncher = GenericEmulatorPlugin.launch_game(self,myresult[0]["hash_digest"])
        asyncio.run(functionLauncher)
        #TODO implement tests
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()