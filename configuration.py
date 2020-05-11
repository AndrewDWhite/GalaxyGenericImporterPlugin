'''
Created on May 9, 2020

@author: Andrew David White
'''
from galaxyutils.config_parser import get_config_options, Option
import logging
import os

#TODO implement or remove 

class Default_Config():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        logging.info("configuring")
        CONFIG_OPTIONS = get_config_options([Option(option_name="log_sensitive_data"),Option(option_name="outputFile"),Option(option_name="outputUserFile")])
        LOG_SENSITIVE_DATA = CONFIG_OPTIONS["log_sensitive_data"]
        self.outputFile=CONFIG_OPTIONS["outputFile"]
        self.outputUserFile=CONFIG_OPTIONS["outputUserFile"]
        logging.info(self.outputFile)
        logging.info(self.outputUserFile)
        #TODO fix the above
        self.outputFile=os.environ['localappdata']+"\\GOG.com\\Galaxy\\plugins\\installed\\importer_97543122-7785-4444-2254-711233556699\\listgames.txt"
        self.outputUserFile=os.environ['localappdata']+"\\GOG.com\\Galaxy\\plugins\\installed\\importer_97543122-7785-4444-2254-711233556699\\listuser.txt"
