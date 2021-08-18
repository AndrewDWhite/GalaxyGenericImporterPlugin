
import os

def run_my_selected_game_here(execution_command, logging):
    my_command = os.system(execution_command)
    logging.debug("rett")
    logging.debug("return value from application: ")
    logging.debug(my_command)
    if (my_command!=0):
        logging.error("There was an issue executing your command check it on the command line manually")
        logging.error(execution_command[1:-1])
    return my_command