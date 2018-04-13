#!/usr/bin/env python3

# from dota2.protobufs.dota_shared_enums_pb2 import DOTA_GC_TEAM, DOTABotDifficulty
from steam import SteamClient
from dota2 import Dota2Client
from dota2.enums import DOTA_GC_TEAM, DOTABotDifficulty

# Setup logging.
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

client = SteamClient()
dota = Dota2Client(client)


@client.on('logged_on')
def start_dota():
    dota.launch()


@dota.on('ready')
def dota_launched():
    # Create game lobby.
    dota.create_practice_lobby()


@dota.on('lobby_new')
def entered_lobby(lobby):
    """
    Entered a lobby event handler (by creating or joining one).
    """

    # Add bots and yourself to lobby.
    dota.join_practice_lobby_team(slot=2,
                                  team=DOTA_GC_TEAM.SPECTATORS)
    dota.add_bot_to_practice_lobby(slot=1,
                                   team=DOTA_GC_TEAM.GOOD_GUYS,
                                   bot_difficulty=DOTABotDifficulty.BOT_DIFFICULTY_EXTRA1)
    dota.add_bot_to_practice_lobby(slot=4, team=DOTA_GC_TEAM.BAD_GUYS,
                                   bot_difficulty=DOTABotDifficulty.BOT_DIFFICULTY_PASSIVE)

    # Launch game.
    dota.launch_practice_lobby({'fill_with_bots': True})


def main():
    # FIXME DO NOT PUBLISH
    client.cli_login(username='vergiliy57', password='575Vfcnth')
    client.run_forever()


if __name__ == '__main__':
    main()
