
from galaxy.api.types import Game, LicenseInfo, LicenseType

from escapejson import escapejson

async def create_game(game):
    my_hash = escapejson(game["hash_digest"])
    my_game_name = escapejson(game["game_name"])
    return Game(my_hash, my_game_name, None, LicenseInfo(LicenseType.SinglePurchase))
