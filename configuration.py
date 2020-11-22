'''
Created on May 9, 2020

@author: Andrew David White
'''
from galaxyutils.config_parser import  Option, get_config_options
import logging

#TODO implement or remove 

class DefaultConfig():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        logging.info("configuring")
        my_options = [Option(option_name="user",str_option=True), Option(option_name="platform",str_option=True)]
        CONFIG_OPTIONS = get_config_options(my_options)
        logging.info(CONFIG_OPTIONS)
        self.my_user_to_gog=CONFIG_OPTIONS["user"]
        self.my_platform_to_gog=CONFIG_OPTIONS["platform"]
        