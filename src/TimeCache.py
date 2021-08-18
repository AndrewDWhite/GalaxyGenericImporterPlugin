import logging
from TimeUtils import time_delta_calc_minutes
from LocalCache import update_cache_time
from galaxy.api.types import GameTime

import math

from escapejson import escapejson

async def finished_game_run(self, start_time, game_id, local_time_cache):
    logging.debug("game finished")
    logging.debug(game_id)
    my_delta = await time_delta_calc_minutes(start_time)
    logging.debug(my_delta)
    my_cache_update =[]
    placed_game = False
    for current_game in local_time_cache:
        if current_game["hash_digest"] == game_id:
            logging.debug("game play time updated")
            logging.debug(game_id)
            #update it if it exists in some form
            my_game_update = await created_update(current_game, my_delta, start_time)
            placed_game = True
            my_cache_update.append(my_game_update)
        else:
            #This entry doesn't need an update
            my_cache_update.append(current_game)
    if not placed_game:
        #new entry to be placed
        logging.debug("game played for the first time")
        my_game_update = {} 
        my_game_update["run_time_total"] = my_delta
        my_game_update["last_time_played"] = math.floor(start_time.timestamp() )
        my_game_update["hash_digest"] = game_id
        my_cache_update.append(my_game_update)
    await update_cache_time(self, my_cache_update, self.backend.cache_times_filepath)
    my_game_id = escapejson(game_id)
    self.backend.my_queue_update_game_time.put(GameTime(my_game_id, my_game_update["run_time_total"], my_game_update["last_time_played"]))

async def created_update(current_game, my_delta, start_time):
    my_game_update = current_game.copy()
    if "run_time_total" in current_game.keys():
        logging.debug("updated play time")
        my_game_update["run_time_total"] = current_game["run_time_total"] + my_delta
    else:
        logging.debug("new play time")
        my_game_update["run_time_total"] = my_delta
    my_game_update["last_time_played"] = math.floor(start_time.timestamp() )
    return my_game_update
