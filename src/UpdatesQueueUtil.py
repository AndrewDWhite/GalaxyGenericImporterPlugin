import logging
from galaxy.api.consts import LocalGameState
from galaxy.api.types import LocalGame
from GalaxyPluginUtils import create_game

from LocalCache import update_cache

async def state_changed(self, old_dict, new_dict):
    # state changed
    for my_id in new_dict.keys() & old_dict.keys():
        if new_dict[my_id] != old_dict[my_id]:
            logging.debug("changed")
            self.backend.my_queue_update_local_game_status.put(LocalGame(my_id, new_dict[my_id]))
            
async def prepare_to_send_my_updates(self, new_local_games_list, local_game_cache):
    logging.debug("sending updates")
    for entry in new_local_games_list:
        if("local_game_state" not in entry):
            #If we haven't added the game and we want it to count as installed
            if (entry["gameShouldBeInstalled"]):
                logging.debug("Here and installed")
                entry["local_game_state"]=LocalGameState.Installed
            else:
                logging.debug("Here but not installed")
                entry["local_game_state"]=LocalGameState.None_
    state_changes = await get_state_changes(local_game_cache, new_local_games_list)
    await setup_queue_to_send_those_changes(self, new_local_games_list, state_changes["old"], state_changes["new"])
    await update_cache(self, new_local_games_list)
    
async def get_state_changes(old_list, new_list):
    logging.debug("get changes")
    logging.debug(old_list)
    old_dict = {}
    new_dict = {}
    for current_entry in old_list:
        if ("local_game_state" in list(current_entry.keys()) and "hash_digest" in list(current_entry.keys()) ):
            old_dict[current_entry["hash_digest"]] = current_entry["local_game_state"]
    for current_entry in new_list:
        if ("local_game_state" in list(current_entry.keys()) and "hash_digest" in list(current_entry.keys()) ):
            new_dict[current_entry["hash_digest"]] = current_entry["local_game_state"]
    
    result = {"old":old_dict,"new":new_dict}
    return result

    
async def setup_queue_to_send_those_changes(self, new_list, old_dict, new_dict):
    await removed_games(self, old_dict, new_dict)    
    await added_games(self, new_list, old_dict, new_dict)                
    await state_changed(self, old_dict, new_dict)
    logging.debug("done updates")
    
async def removed_games(self, old_dict, new_dict):
    # removed games
    for my_id in (old_dict.keys() - new_dict.keys()):
        logging.debug("removed")
        self.backend.my_queue_update_local_game_status.put(LocalGame(my_id, LocalGameState.None_))

async def added_games(self, new_list, old_dict, new_dict):
    # added games
    for local_game in new_list:
        if ("hash_digest" in local_game) and (local_game["hash_digest"] in (new_dict.keys() - old_dict.keys())):
            logging.debug("added")
            my_created_game = await create_game(local_game)
            self.backend.my_queue_add_game.put(my_created_game)
            self.backend.my_queue_update_local_game_status.put(LocalGame(local_game["hash_digest"], local_game["local_game_state"]))



