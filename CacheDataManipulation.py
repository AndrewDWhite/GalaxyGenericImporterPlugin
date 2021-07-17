import logging

from escapejson import escapejson

async def get_exe_command(game_id,local_game_cache):
    my_game_to_launch={}
    for current_game_checking in local_game_cache:
        my_hash = escapejson(current_game_checking["hash_digest"])
        if (my_hash == game_id):
            my_game_to_launch =  current_game_checking
            break      
    logging.debug(my_game_to_launch)
    execution_command = ""
    if "execution" in my_game_to_launch.keys():
        my_replaced_game_to_launch = my_game_to_launch["execution"]
        my_replaced_game_to_launch = my_replaced_game_to_launch.replace("%ROM_RAW%", my_game_to_launch["filename"])
        my_replaced_game_to_launch = my_replaced_game_to_launch.replace("%ROM_DIR%", my_game_to_launch["path"])
        if None == my_game_to_launch["game_filename"]:
            logging.error("Invalid game_filename")
            logging.error(my_game_to_launch)
        my_replaced_game_to_launch = my_replaced_game_to_launch.replace("%ROM_NAME%", my_game_to_launch["game_filename"])
        execution_command="\""+my_replaced_game_to_launch+"\""
        logging.debug("starting")
        logging.debug(execution_command)
    return execution_command